package com.neurokey.keyboard

import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.LinearGradient
import android.graphics.Paint
import android.graphics.Path
import android.graphics.Shader
import android.util.AttributeSet
import android.view.animation.LinearInterpolator
import android.widget.LinearLayout
import kotlin.math.sin

class WaveKeyboardLayout @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : LinearLayout(context, attrs) {
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val wavePath = Path()
    private var phase = 0f
    private var animator: ValueAnimator? = null

    init {
        setWillNotDraw(false)
        orientation = VERTICAL
        setLayerType(LAYER_TYPE_SOFTWARE, null)
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        animator = ValueAnimator.ofFloat(0f, (Math.PI * 2).toFloat()).apply {
            duration = 9000L
            repeatCount = ValueAnimator.INFINITE
            interpolator = LinearInterpolator()
            addUpdateListener {
                phase = it.animatedValue as Float
                invalidate()
            }
            start()
        }
    }

    override fun onDetachedFromWindow() {
        animator?.cancel()
        animator = null
        super.onDetachedFromWindow()
    }

    override fun onDraw(canvas: Canvas) {
        val theme = context.getSharedPreferences("neurokey_preferences", Context.MODE_PRIVATE)
            .getString("keyboard_theme", "ocean")
        val colors = when (theme) {
            "sunset" -> intArrayOf(Color.rgb(48, 12, 62), Color.rgb(145, 42, 78), Color.rgb(240, 119, 70))
            "forest" -> intArrayOf(Color.rgb(4, 35, 29), Color.rgb(12, 91, 69), Color.rgb(77, 157, 89))
            else -> intArrayOf(Color.rgb(4, 17, 39), Color.rgb(11, 58, 91), Color.rgb(10, 126, 153))
        }
        paint.shader = LinearGradient(0f, 0f, width.toFloat(), height.toFloat(), colors, null, Shader.TileMode.CLAMP)
        canvas.drawRect(0f, 0f, width.toFloat(), height.toFloat(), paint)
        paint.shader = null
        drawWave(canvas, height * 0.28f, height * 0.13f, 0.010f, Color.argb(60, 96, 220, 255))
        drawWave(canvas, height * 0.62f, height * 0.11f, 0.014f, Color.argb(45, 196, 119, 255))
        drawWave(canvas, height * 0.88f, height * 0.08f, 0.018f, Color.argb(40, 53, 235, 170))
    }

    private fun drawWave(canvas: Canvas, centerY: Float, amplitude: Float, frequency: Float, color: Int) {
        wavePath.reset()
        wavePath.moveTo(0f, centerY)
        var x = 0f
        while (x <= width.toFloat()) {
            val y = centerY + (sin(x * frequency + phase) * amplitude)
            wavePath.lineTo(x, y.toFloat())
            x += 8f
        }
        wavePath.lineTo(width.toFloat(), height.toFloat())
        wavePath.lineTo(0f, height.toFloat())
        wavePath.close()
        paint.color = color
        canvas.drawPath(wavePath, paint)
    }
}