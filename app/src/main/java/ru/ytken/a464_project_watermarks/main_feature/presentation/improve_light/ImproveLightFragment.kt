package ru.ytken.a464_project_watermarks.main_feature.presentation.improve_light

import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.os.bundleOf
import androidx.fragment.app.setFragmentResult
import androidx.fragment.app.setFragmentResultListener
import androidx.navigation.fragment.findNavController
import kotlinx.android.synthetic.main.fragment_image_result.*
import ru.ytken.a464_project_watermarks.R
import ru.ytken.a464_project_watermarks.main_feature.utils.BitmapExtensions.makeImageSharpGaussian
import ru.ytken.a464_project_watermarks.main_feature.utils.BitmapExtensions.setBrightnessContrast
import java.io.ByteArrayOutputStream
import java.io.File
import java.util.*

class ImproveLightFragment : Fragment(R.layout.fragment_improve_light) {

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setFragmentResultListener("fromCropToLight") {
                _, bun ->
            val str = bun.getString("uri")
            val uri = Uri.parse(
                str
            )
            val bitmap = MediaStore.Images.Media.getBitmap(requireActivity().contentResolver, uri)
            val bitmapp = bitmap.setBrightnessContrast()
            imageViewResultImage.setImageBitmap(bitmapp)
            buttonSeeSkan.setOnClickListener {
                val bytes = ByteArrayOutputStream()
                if (bitmapp != null) {
                    bitmapp.compress(Bitmap.CompressFormat.JPEG, 100, bytes)
                }
                val path: String = MediaStore.Images.Media.insertImage(
                    requireActivity().contentResolver,
                    bitmapp,
                    "IMG_" + Calendar.getInstance().time,
                    null
                )
                val uri = Uri.parse(path)
                setFragmentResult(
                    "fromLightToImage",
                    bundleOf("uri" to uri.toString())
                )
                findNavController().navigate(R.id.action_improveLightFragment_to_imageResultFragment)
            }
        }
        imageButtonClose.setOnClickListener {
            findNavController().popBackStack()
        }
    }
}