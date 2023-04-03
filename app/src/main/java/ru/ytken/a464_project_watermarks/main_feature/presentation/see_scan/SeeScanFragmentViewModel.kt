package ru.ytken.a464_project_watermarks.main_feature.presentation.see_scan

import android.content.Context
import android.database.Cursor
import android.net.Uri
import android.provider.MediaStore
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel


class SeeScanFragmentViewModel: ViewModel() {
    private val liveScanLettersText = MutableLiveData<String>()

    var lineBounds: ArrayList<Int> = ArrayList()

    fun setLetterText(text: String) {
        liveScanLettersText.value = text
    }

    fun getFilePath(uri: Uri, context: Context): String? {
        val projection = arrayOf(MediaStore.Images.Media.DATA)
        val cursor: Cursor? = context.contentResolver.query(uri, projection, null, null, null)
        if (cursor != null) {
            cursor.moveToFirst()
            val columnIndex: Int = cursor.getColumnIndex(projection[0])
            val picturePath: String = cursor.getString(columnIndex) // returns null
            cursor.close()
            return picturePath
        }
        return null
    }
}
