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

interface NlpApiService {
    @POST("/api/v1/predict/next-word")
    suspend fun getNextWord(@Body request: PredictWordRequest): PredictWordResponse
}

object ApiClient {
    const val DEFAULT_BASE_URL = "http://10.0.2.2:8000"
    const val PREFERENCES_NAME = "neurokey_preferences"
    const val BACKEND_URL_KEY = "backend_url"

    private val client = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(10, TimeUnit.SECONDS)
        .build()

    fun apiService(context: Context): NlpApiService {
        val preferences = context.getSharedPreferences(PREFERENCES_NAME, Context.MODE_PRIVATE)
        val configuredUrl = preferences.getString(BACKEND_URL_KEY, DEFAULT_BASE_URL)
            ?.trim()
            ?.trimEnd('/')
            .orEmpty()
        val baseUrl = if (configuredUrl.isBlank()) DEFAULT_BASE_URL else configuredUrl

        return Retrofit.Builder()
            .baseUrl("$baseUrl/")
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(NlpApiService::class.java)
    }
}
