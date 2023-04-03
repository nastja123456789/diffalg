package ru.ytken.a464_project_watermarks.main_feature.presentation.see_scan.utils

import android.util.Log
import java.util.*
import kotlin.collections.ArrayList

import kotlin.math.sqrt
import org.apache.commons.math3.linear.*
import org.apache.commons.math3.distribution.MultivariateNormalDistribution
import kotlin.math.*

object Watermarks {
//    fun gmm_alg(M: DoubleArray): String {
//        val x = Array2DRowRealMatrix(M.mapIndexed { i, a -> doubleArrayOf(i.toDouble(), a * a) }.toTypedArray())
//        val gm = GaussianMixture(2, 1e-6.toInt(), 1000.0)
//        gm.fit(x)
//        val clusters = gm.cluster(x)
//        val first: MutableList<Double> = ArrayList()
//        val zeros: MutableList<Double> = ArrayList()
//        for (i in 0 until clusters.length) {
//            if (clusters.get(i) === 1) {
//                first.add(M[i])
//            } else {
//                zeros.add(M[i])
//            }
//        }
//        var watermark = ""
//        if (StatUtils.mode(zeros.stream().mapToDouble { obj: Double -> obj }
//                .toArray()) > StatUtils.mode(first.stream().mapToDouble { obj: Double -> obj }
//                .toArray())) {
//            for (j in clusters) {
//                watermark += if (j == 0) {
//                    "1"
//                } else {
//                    "0"
//                }
//            }
//        } else {
//            for (j in clusters) {
//                watermark += if (j == 0) {
//                    "0"
//                } else {
//                    "1"
//                }
//            }
//        }
//
//        return watermark
//    }

    fun getWatermark(lineBounds: ArrayList<Int>): String? {
        val meanInterval = lineBounds.mean()
        Log.d("$meanInterval","33333")
        val stdIntervals = lineBounds.std()
        if (stdIntervals < 0.4) return null
        var watermark = ""
        for (i in lineBounds)
            if (i > meanInterval + stdIntervals*0.7) {
                watermark += "1"
            }
            else {
                watermark += 0
            }
        return watermark
    }

    private fun ArrayList<Int>.mean(): Float = this.sum().toFloat() / this.size

    private fun ArrayList<Int>.std(): Float {
        val mean = this.mean()
        var sqSum = 0f
        for (i in this) sqSum += (i - mean)*(i - mean)
        sqSum /= this.size
        return sqrt(sqSum)
    }
}
