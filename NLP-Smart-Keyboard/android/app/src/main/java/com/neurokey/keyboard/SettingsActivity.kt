package com.neurokey.keyboard

import android.app.Activity
import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.graphics.Color
import android.view.Gravity
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import com.neurokey.keyboard.api.ApiClient
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class SettingsActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val preferences = getSharedPreferences(ApiClient.PREFERENCES_NAME, MODE_PRIVATE)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 32, 32, 32)
        }
        root.addView(TextView(this).apply {
            text = "NeuroKey Settings\nEnable the keyboard in system settings."
            textSize = 20f
        })
        val urlInput = EditText(this).apply {
            hint = "Backend URL"
            setSingleLine(true)
            setText(preferences.getString(ApiClient.BACKEND_URL_KEY, ApiClient.DEFAULT_BASE_URL))
        }
        root.addView(urlInput)
        val themeInput = EditText(this).apply {
            hint = "Theme: ocean, sunset, or forest"
            setSingleLine(true)
            setText(preferences.getString(ApiClient.THEME_KEY, "ocean"))
        }
        root.addView(themeInput)
        val displayModeInput = EditText(this).apply {
            hint = "Display: auto, day, or night"
            setSingleLine(true)
            setText(preferences.getString(ApiClient.DISPLAY_MODE_KEY, "auto"))
        }
        root.addView(displayModeInput)
        val sizeInput = EditText(this).apply {
            hint = "Keyboard size: compact, standard, or large"
            setSingleLine(true)
            setText(preferences.getString(ApiClient.KEYBOARD_SIZE_KEY, "standard"))
        }
        root.addView(sizeInput)
        root.addView(Button(this).apply {
            text = "Allow voice input"
            setOnClickListener {
                if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), 100)
                }
            }
        })
        root.addView(Button(this).apply {
            text = "Save backend URL"
            setOnClickListener {
                preferences.edit()
                    .putString(ApiClient.BACKEND_URL_KEY, urlInput.text.toString().trim().trimEnd('/'))
                    .apply()
            }
        })
        root.addView(Button(this).apply {
            text = "Save theme"
            setOnClickListener {
                val theme = themeInput.text.toString().trim().lowercase()
                preferences.edit().putString(ApiClient.THEME_KEY, theme.ifBlank { "ocean" }).apply()
            }
        })
        root.addView(Button(this).apply {
            text = "Save display and size"
            setOnClickListener {
                val mode = displayModeInput.text.toString().trim().lowercase()
                val size = sizeInput.text.toString().trim().lowercase()
                preferences.edit()
                    .putString(ApiClient.DISPLAY_MODE_KEY, mode.ifBlank { "auto" })
                    .putString(ApiClient.KEYBOARD_SIZE_KEY, size.ifBlank { "standard" })
                    .apply()
            }
        })
        val status = TextView(this).apply {
            gravity = Gravity.CENTER_VERTICAL
            setTextColor(Color.DKGRAY)
        }
        root.addView(status)
        root.addView(Button(this).apply {
            text = "Test connection"
            setOnClickListener {
                preferences.edit()
                    .putString(ApiClient.BACKEND_URL_KEY, urlInput.text.toString().trim().trimEnd('/'))
                    .apply()
                status.text = "Testing..."
                CoroutineScope(Dispatchers.IO).launch {
                    val result = runCatching {
                        ApiClient.apiService(this@SettingsActivity).getNextWord(
                            com.neurokey.keyboard.api.PredictWordRequest("hello", 1)
                        )
                    }
                    runOnUiThread {
                        status.text = if (result.isSuccess) "Connection successful" else "Connection unavailable"
                    }
                }
            }
        })
        setContentView(root)
    }
}
