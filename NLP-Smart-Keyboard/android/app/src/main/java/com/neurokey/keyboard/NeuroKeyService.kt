package com.neurokey.keyboard

import android.inputmethodservice.InputMethodService
import android.text.InputType
import android.view.KeyEvent
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.LinearLayout
import com.neurokey.keyboard.api.ApiClient
import com.neurokey.keyboard.api.PredictSentenceRequest
import com.neurokey.keyboard.api.PredictWordRequest
import com.neurokey.keyboard.api.TextRequest
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class NeuroKeyService : InputMethodService(), View.OnClickListener {
    private lateinit var keyboardView: LinearLayout
    private lateinit var suggestion1: Button
    private lateinit var suggestion2: Button
    private lateinit var suggestion3: Button
    private lateinit var shiftButton: Button
    private lateinit var modeButton: Button
    private var sensitiveField = false
    private var shifted = false
    private var symbols = false
    private var requestJob: Job? = null
    private val serviceScope = CoroutineScope(Dispatchers.Main + Job())

    override fun onCreateInputView(): View {
        keyboardView = layoutInflater.inflate(R.layout.keyboard_view, null) as LinearLayout
        suggestion1 = keyboardView.findViewById(R.id.suggestion_1)
        suggestion2 = keyboardView.findViewById(R.id.suggestion_2)
        suggestion3 = keyboardView.findViewById(R.id.suggestion_3)
        shiftButton = keyboardView.findViewById(R.id.btn_shift)
        modeButton = keyboardView.findViewById(R.id.btn_mode)
        suggestion1.setOnClickListener { insertSuggestion(suggestion1.text.toString()) }
        suggestion2.setOnClickListener { insertSuggestion(suggestion2.text.toString()) }
        suggestion3.setOnClickListener { insertSuggestion(suggestion3.text.toString()) }
        bindButtons(keyboardView)
        return keyboardView
    }

    private fun bindButtons(view: View) {
        if (view is Button && view.id !in setOf(R.id.suggestion_1, R.id.suggestion_2, R.id.suggestion_3)) {
            view.setOnClickListener(this)
        } else if (view is android.view.ViewGroup) {
            for (index in 0 until view.childCount) bindButtons(view.getChildAt(index))
        }
    }

    override fun onStartInputView(info: EditorInfo?, restarting: Boolean) {
        super.onStartInputView(info, restarting)
        sensitiveField = isSensitiveInputType(info?.inputType ?: 0)
        shifted = false
        symbols = false
        updateLabels()
        if (sensitiveField) clearSuggestions("Secured field") else fetchSuggestions()
    }

    private fun isSensitiveInputType(inputType: Int): Boolean {
        val type = inputType and InputType.TYPE_MASK_CLASS
        val variation = inputType and InputType.TYPE_MASK_VARIATION
        return (type == InputType.TYPE_CLASS_TEXT && variation in setOf(
            InputType.TYPE_TEXT_VARIATION_PASSWORD,
            InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD,
            InputType.TYPE_TEXT_VARIATION_WEB_PASSWORD
        )) || (type == InputType.TYPE_CLASS_NUMBER && variation == InputType.TYPE_NUMBER_VARIATION_PASSWORD)
    }

    override fun onClick(view: View?) {
        val button = view as? Button ?: return
        val connection = currentInputConnection ?: return
        when (button.id) {
            R.id.btn_delete -> connection.deleteSurroundingText(1, 0)
            R.id.btn_enter -> connection.sendKeyEvent(KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_ENTER))
            R.id.btn_space -> connection.commitText(" ", 1)
            R.id.btn_shift -> { shifted = !shifted; updateLabels() }
            R.id.btn_mode -> { symbols = !symbols; updateLabels() }
            R.id.btn_emoji -> showEmojiSuggestions()
            R.id.btn_sentence -> showSentenceSuggestions()
            else -> {
                val text = button.text.toString()
                if (text.isNotEmpty()) connection.commitText(if (!symbols && shifted) text.uppercase() else text, 1)
                if (shifted) { shifted = false; updateLabels() }
            }
        }
        if (button.id !in setOf(R.id.btn_shift, R.id.btn_mode, R.id.btn_emoji, R.id.btn_sentence)) fetchSuggestions()
    }

    private fun updateLabels() {
        modeButton.text = if (symbols) "ABC" else "123"
        shiftButton.text = if (shifted) "SHIFT" else "shift"
        val row = keyboardView.findViewWithTag<LinearLayout>("letter_row") ?: return
        for (index in 0 until row.childCount) {
            val button = row.getChildAt(index) as? Button ?: continue
            button.text = if (!symbols && shifted) button.text.toString().uppercase() else button.text.toString().lowercase()
        }
    }

    private fun insertSuggestion(value: String) {
        if (value.isBlank() || value == "Secured field" || value == "Offline") return
        val connection = currentInputConnection ?: return
        val before = connection.getTextBeforeCursor(1, 0)?.toString().orEmpty()
        connection.commitText(if (before.isNotEmpty() && !before.endsWith(" ")) " $value " else "$value ", 1)
        fetchSuggestions()
    }

    private fun fetchSuggestions() {
        if (sensitiveField) return
        requestJob?.cancel()
        requestJob = serviceScope.launch {
            delay(250)
            val text = currentInputConnection?.getTextBeforeCursor(80, 0)?.toString().orEmpty()
            if (text.isBlank()) { clearSuggestions(); return@launch }
            try {
                val response = ApiClient.apiService(this@NeuroKeyService).getNextWord(PredictWordRequest(text, 3))
                val words = response.predictions.map { it.word }.filter { it.isNotBlank() }
                if (words.isEmpty()) showOfflineSuggestions(text) else setSuggestions(words)
            } catch (_: Exception) { showOfflineSuggestions(text) }
        }
    }

    private fun showSentenceSuggestions() {
        val text = currentInputConnection?.getTextBeforeCursor(160, 0)?.toString().orEmpty()
        if (text.isBlank() || sensitiveField) return
        serviceScope.launch {
            try {
                val response = ApiClient.apiService(this@NeuroKeyService).getNextSentence(PredictSentenceRequest(text, 3))
                setSuggestions(response.predictions.map { it.sentence }.filter { it.isNotBlank() })
            } catch (_: Exception) { setSuggestions(listOf("Tell me more.", "That sounds good.", "I will get back to you.")) }
        }
    }

    private fun showEmojiSuggestions() {
        if (sensitiveField) return
        val text = currentInputConnection?.getTextBeforeCursor(160, 0)?.toString().orEmpty()
        serviceScope.launch {
            try {
                val response = ApiClient.apiService(this@NeuroKeyService).getEmojis(TextRequest(text))
                setSuggestions(response.emojis)
            } catch (_: Exception) { setSuggestions(listOf("😊", "👍", "🎉")) }
        }
    }

    private fun showOfflineSuggestions(text: String) {
        val lower = text.lowercase()
        val values = when {
            lower.endsWith("i am going") -> listOf("home", "there", "to")
            lower.endsWith("are you") -> listOf("coming", "okay", "ready")
            lower.endsWith("thank") -> listOf("you", "you!", "you so much")
            else -> listOf("the", "to", "and")
        }
        setSuggestions(values)
    }

    private fun setSuggestions(values: List<String>) {
        listOf(suggestion1, suggestion2, suggestion3).forEachIndexed { index, button ->
            button.text = values.getOrNull(index).orEmpty()
            button.isEnabled = button.text.isNotBlank()
        }
    }

    private fun clearSuggestions(message: String = "") = setSuggestions(listOf(message))

    override fun onDestroy() {
        requestJob?.cancel()
        serviceScope.cancel()
        super.onDestroy()
    }
}
