package com.neurokey.keyboard.api

import android.content.Context
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST
import okhttp3.OkHttpClient
import java.util.concurrent.TimeUnit

data class PredictWordRequest(val text: String, val top_k: Int = 3)
data class PredictWordResponse(val predictions: List<Prediction>)
data class Prediction(val word: String, val probability: Double, val model: String)
data class PredictSentenceRequest(val context: String, val top_k: Int = 3)
data class PredictSentenceResponse(val predictions: List<SentencePrediction>)
data class SentencePrediction(val sentence: String, val score: Double = 0.0)
data class TextRequest(val text: String)
data class EmojiResponse(val emojis: List<String>)
data class GifResponse(val query: String, val url: String? = null, val message: String? = null)

interface NlpApiService {
    @POST("/api/v1/predict/next-word")
    suspend fun getNextWord(@Body request: PredictWordRequest): PredictWordResponse

    @POST("/api/v1/predict/next-sentence")
    suspend fun getNextSentence(@Body request: PredictSentenceRequest): PredictSentenceResponse

    @POST("/api/v1/nlp/emoji")
    suspend fun getEmojis(@Body request: TextRequest): EmojiResponse

    @POST("/api/v1/nlp/gif")
    suspend fun getGif(@Body request: TextRequest): GifResponse
}

object ApiClient {
    const val DEFAULT_BASE_URL = "http://10.0.2.2:8000"
    const val PREFERENCES_NAME = "neurokey_preferences"
    const val BACKEND_URL_KEY = "backend_url"
    const val THEME_KEY = "keyboard_theme"
    const val DISPLAY_MODE_KEY = "display_mode"
    const val KEYBOARD_SIZE_KEY = "keyboard_size"
    const val AI_ENABLED_KEY = "ai_enabled"

    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    fun apiService(context: Context): NlpApiService {
        val preferences = context.getSharedPreferences(PREFERENCES_NAME, Context.MODE_PRIVATE)
        val configuredUrl = preferences.getString(BACKEND_URL_KEY, DEFAULT_BASE_URL)
            ?.trim()
            ?.trimEnd('/')
            .orEmpty()
        val baseUrl = (if (configuredUrl.isBlank()) DEFAULT_BASE_URL else configuredUrl)
            .removeSuffix("/api/v1")
            .trimEnd('/')

        return Retrofit.Builder()
            .baseUrl("$baseUrl/")
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(NlpApiService::class.java)
    }
}
