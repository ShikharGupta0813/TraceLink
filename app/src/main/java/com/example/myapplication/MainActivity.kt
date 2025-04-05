package com.example.myapplication

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.provider.CallLog
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    private val REQUEST_CALL_LOG = 1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val callLogButton = findViewById<Button>(R.id.call_log_btn)
        callLogButton.setOnClickListener {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CALL_LOG)
                != PackageManager.PERMISSION_GRANTED) {
                // Ask for permission
                ActivityCompat.requestPermissions(this,
                    arrayOf(Manifest.permission.READ_CALL_LOG),
                    REQUEST_CALL_LOG)
            } else {
                // Permission already granted
                getCallLogs()
            }
        }
    }

    private fun getCallLogs() {
        val cursor = contentResolver.query(
            CallLog.Calls.CONTENT_URI,
            null,
            null,
            null,
            CallLog.Calls.DATE + " DESC"
        )

        val stringBuilder = StringBuilder()

        if (cursor != null && cursor.moveToFirst()) {
            do {
                val number = cursor.getString(cursor.getColumnIndexOrThrow(CallLog.Calls.NUMBER))
                val type = cursor.getString(cursor.getColumnIndexOrThrow(CallLog.Calls.TYPE))
                val date = cursor.getString(cursor.getColumnIndexOrThrow(CallLog.Calls.DATE))
                val duration = cursor.getString(cursor.getColumnIndexOrThrow(CallLog.Calls.DURATION))


                stringBuilder.append("Number: $number\nType: $type\nDate: $date\nDuration: $duration sec\n\n")
            } while (cursor.moveToNext())

            cursor.close()
        }

        Toast.makeText(this, stringBuilder.toString(), Toast.LENGTH_LONG).show()
    }

    // Handle permission result
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        if (requestCode == REQUEST_CALL_LOG) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                getCallLogs()
            } else {
                Toast.makeText(this, "Permission denied to read call logs", Toast.LENGTH_SHORT).show()
            }
        }
    }
}