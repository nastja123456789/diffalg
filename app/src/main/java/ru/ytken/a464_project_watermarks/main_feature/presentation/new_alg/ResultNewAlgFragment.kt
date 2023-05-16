package ru.ytken.a464_project_watermarks.main_feature.presentation.new_alg

import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.setFragmentResultListener
import androidx.fragment.app.viewModels
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.android.synthetic.main.fragment_result_new_alg.*
import kotlinx.android.synthetic.main.fragment_scan_result.*
import kotlinx.android.synthetic.main.fragment_scan_result.imageViewCopyToBuffer
import kotlinx.android.synthetic.main.fragment_scan_result.imageViewSkanned
import kotlinx.android.synthetic.main.fragment_scan_result.progressBarWaitForScan
import kotlinx.android.synthetic.main.fragment_scan_result.textViewProgress
import kotlinx.android.synthetic.main.fragment_scan_result.textViewRecognizedText
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import ru.ytken.a464_project_watermarks.R
import ru.ytken.a464_project_watermarks.main_feature.domain.use_cases.SavedImageFactoryUseCase
import ru.ytken.a464_project_watermarks.main_feature.utils.BitmapExtensions.toGrayscale
import java.io.File
import kotlin.math.sqrt

class ResultNewAlgFragment : Fragment(R.layout.fragment_result_new_alg) {
    private val vm: NewAlgFragmentViewModel by viewModels {
        SavedImageFactoryUseCase()
    }
    private var fileWithImage: Bitmap? = null
    private var avg: ArrayList<Int> = ArrayList()
    private var avgLine: ArrayList<ArrayList<Int>> = ArrayList()
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setFragmentResultListener("fromNewAlgToResultNewAlg") {
                _, bun ->
            val str = bun.getString("uri")
            val uri = Uri.parse(
                str
            )
            fileWithImage = MediaStore.Images.Media.getBitmap(requireActivity().contentResolver, uri)
            imageViewSkanned.setImageBitmap(fileWithImage)
            if (fileWithImage != null) {
                Log.d("lllll","lllll")
                processImage(fileWithImage!!.toGrayscale()!!)
            }
            val fdelete = vm.getFilePath(uri, requireContext())?.let { File(it) }
            if (fdelete!!.exists()) {
                if (fdelete.delete()) {
                } else {
                }
            }
        }
        setFragmentResultListener("arrayListArrayList") {
                _, bun ->
            vm.lineBounds = bun.getSerializable("arrayList") as ArrayList<ArrayList<Int>>
        }
        imageButtonClosing.setOnClickListener {
            findNavController().popBackStack(R.id.buttonFragment, true)
            findNavController().navigate(R.id.buttonFragment)
        }
    }

    private fun processImage(fileWithImage: Bitmap) = lifecycleScope.launch(Dispatchers.Main) {
        progressBarWaitForScan.visibility = View.VISIBLE
        textViewProgress.visibility = View.VISIBLE
        textViewProgress.text = getString(R.string.ScanningImage)
        val lineBounds = vm.lineBounds

        fileWithImage.let {
            imageButtonClosing.visibility = View.VISIBLE
            val watermarkSize = 24
            val resMatrix = ""
            if (lineBounds.isEmpty()) {
                Log.d("pppppp","pppppp")
            }
            Log.d("alalalala","${lineBounds.size}")
            try{
                val lineIntervals = ArrayList<ArrayList<Int>>()
                for (line in lineBounds) {
                    if (line.size%8!=0) {
                        val lenth = line.size-line.size%8
                        var mut: java.util.ArrayList<Int> = line
                        var mutty: MutableList<Int> = mut.toMutableList()
                        mutty = mut.subList(0, lenth)
                        val arr: ArrayList<Int> = ArrayList(mutty)
                        lineIntervals.add(arr)
                        val num = arr.chunked(8)
                        for (i in num) {
                            avg.add(i.average().toInt())
                        }
                        avgLine.add(avg)
                    } else {
                        lineIntervals.add(line)
                        val num = line.chunked(8)
                        for (i in num) {
                            avg.add(i.average().toInt())
                        }
                        avgLine.add(avg)
                    }
                }
                for (i in avg) {
                    Log.d("$i","iiiii")
                }
                val result = res(avg)
                setTextButton(result.subSequence(0,24).toString())
                vm.setLetterText(resMatrix)
                val res = vm.compareStrings(result.subSequence(0,watermarkSize).toString())
                Toast.makeText(context, "$res %", Toast.LENGTH_SHORT).show()
            } catch (e: java.lang.IndexOutOfBoundsException) {
                Toast.makeText(context, "К сожалению изображение не содержит водяной знак!", Toast.LENGTH_SHORT).show()
            }
            progressBarWaitForScan.visibility = View.INVISIBLE
            textViewProgress.visibility = View.INVISIBLE

        }
    }

    private fun res(line: ArrayList<Int>): String {
        val meanInterval = line.mean()
        val stdIntervals = line.std()
        var watermark = ""
        for (i in line)
            if (i > meanInterval + stdIntervals*0.35) {
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

    private fun setTextButton(text: String) {
        textViewRecognizedText.visibility = View.VISIBLE
        imageViewCopyToBuffer.visibility = View.VISIBLE
        textViewRecognizedText.text = text
    }

    override fun onDestroyView() {
        super.onDestroyView()
    }
}