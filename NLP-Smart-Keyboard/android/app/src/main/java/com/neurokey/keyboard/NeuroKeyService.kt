package com.neurokey.keyboard

import android.inputmethodservice.InputMethodService
import android.text.InputType
import android.view.KeyEvent
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.LinearLayout
import kotlinx.coroutines.*
import com.neurokey.keyboard.api.ApiClient
import com.neurokey.keyboard.api.PredictWordRequest

class NeuroKeyService : InputMethodService(), View.OnClickListener {

    private lateinit var keyboardView: LinearLayout
    private lateinit var suggestion1: Button
    private lateinit var suggestion2: Button
    private lateinit var suggestion3: Button
    private val serviceJob = Job()
    private val coroutineScope = CoroutineScope(Dispatchers.Main + serviceJob)
    private var isSensitiveField = false

    override fun onCreateInputView(): View {
        keyboardView = layoutInflater.inflate(R.layout.keyboard_view, null) as LinearLayout
        
        suggestion1 = keyboardView.findViewById(R.id.suggestion_1)
        suggestion2 = keyboardView.findViewById(R.id.suggestion_2)
        suggestion3 = keyboardView.findViewById(R.id.suggestion_3)
        
        suggestion1.setOnClickListener { insertSuggestion(suggestion1.text.toString()) }
        suggestion2.setOnClickListener { insertSuggestion(suggestion2.text.toString()) }
        suggestion3.setOnClickListener { insertSuggestion(suggestion3.text.toString()) }

        // Setup basic letter keys for demo
        val keys = listOf("Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
                         "A", "S", "D", "F", "G", "H", "J", "K", "L",
                         "Z", "X", "C", "V", "B", "N", "M")
        // Call recursive binding method
        setupClickListeners(keyboardView)
        
        return keyboardView
    }

    private fun setupClickListeners(view: View) {
        if (view is Button) {
            // Do not bind the suggestion container buttons, they have their own logic
            if (view.id != R.id.suggestion_1 && view.id != R.id.suggestion_2 && view.id != R.id.suggestion_3) {
                view.setOnClickListener(this)
            }
        } else if (view is android.view.ViewGroup) {
            for (i in 0 until view.childCount) {
                setupClickListeners(view.getChildAt(i))
            }
        }
    }

    override fun onStartInputView(info: EditorInfo?, restarting: Boolean) {
        super.onStartInputView(info, restarting)
        
        // Privacy check
        isSensitiveField = isSensitiveInputType(info?.inputType ?: 0)
        
        if (isSensitiveField) {
            clearSuggestions()
            suggestion2.text = "🔒 Secured Field"
            suggestion1.isEnabled = false
            suggestion2.isEnabled = false
            suggestion3.isEnabled = false
        } else {
            suggestion1.isEnabled = true
            suggestion2.isEnabled = true
            suggestion3.isEnabled = true
            fetchSuggestions()
        }
    }

    private fun isSensitiveInputType(inputType: Int): Boolean {
        val type = inputType and InputType.TYPE_MASK_CLASS
        val variation = inputType and InputType.TYPE_MASK_VARIATION
        
        return type == InputType.TYPE_CLASS_TEXT &&
                (variation == InputType.TYPE_TEXT_VARIATION_PASSWORD ||
                 variation == InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD ||
                 variation == InputType.TYPE_TEXT_VARIATION_WEB_PASSWORD) ||
               type == InputType.TYPE_CLASS_NUMBER &&
                (variation == InputType.TYPE_NUMBER_VARIATION_PASSWORD)
    }

    override fun onClick(v: View?) {
        val ic = currentInputConnection ?: return
        if (v is Button) {
            when (v.id) {
                R.id.btn_delete -> ic.deleteSurroundingText(1, 0)
                R.id.btn_enter -> ic.sendKeyEvent(KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_ENTER))
                R.id.btn_space -> {
                    ic.commitText(" ", 1)
                    fetchSuggestions()
                }
                R.id.btn_dot -> ic.commitText(".", 1)
                else -> {
                    ic.commitText(v.text.toString().lowercase(), 1)
                    fetchSuggestions()
                }
            }
        }
    }

    private fun insertSuggestion(word: String) {
        if (word.isBlank()) return
        val ic = currentInputConnection ?: return
        
        val textBefore = ic.getTextBeforeCursor(1, 0) ?: ""
        if (textBefore.isNotEmpty() && !textBefore.endsWith(" ")) {
            ic.commitText(" $word ", 1)
        } else {
            ic.commitText("$word ", 1)
        }
        clearSuggestions()
    }

    private fun fetchSuggestions() {
        if (isSensitiveField) return
        
        val ic = currentInputConnection ?: return
        val text = ic.getTextBeforeCursor(50, 0)?.toString() ?: return
        
        if (text.isBlank()) {
            clearSuggestions()
            return
        }

        coroutineScope.launch {
            try {
                val response = ApiClient.apiService(this@NeuroKeyService)
                    .getNextWord(PredictWordRequest(text, 3))
                val preds = response.predictions
                
                suggestion1.text = preds.getOrNull(0)?.word ?: ""
                suggestion2.text = preds.getOrNull(1)?.word ?: ""
                suggestion3.text = preds.getOrNull(2)?.word ?: ""
            } catch (e: Exception) {
                // Backend unavailable or network error
                suggestion2.text = "Offline"
            }
        }
    }

    private fun clearSuggestions() {
        suggestion1.text = ""
        suggestion2.text = ""
        suggestion3.text = ""
    }

    override fun onDestroy() {
        super.onDestroy()
        serviceJob.cancel()
    }
}
