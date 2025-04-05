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
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {

    private val REQUEST_CALL_LOG = 1
    private val REQUEST_SMS = 2

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

        val smsButton = findViewById<Button>(R.id.sms_btn)
        smsButton.setOnClickListener {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_SMS)
                != PackageManager.PERMISSION_GRANTED) {

                ActivityCompat.requestPermissions(this,
                    arrayOf(Manifest.permission.READ_SMS),
                    REQUEST_SMS)
            } else {
                getSmsMessages()
            }
        }

    }

    private fun uploadCallLogs(logs: List<Map<String, String>>) {
        Thread {
            try {
                // Calling the upload_call_logs route
                val url = URL("http://10.100.237.49:5000/upload_call_logs/1")
                val conn = url.openConnection() as HttpURLConnection
                conn.requestMethod = "POST"
                conn.setRequestProperty("Content-Type", "application/json; utf-8")
                conn.doOutput = true

                val jsonBody = JSONObject()
                val jsonArray = JSONArray()


                for (log in logs) {
                    val item = JSONObject()
                    item.put("number", log["number"])
                    item.put("type", log["type"])
                    item.put("date", log["date"])
                    item.put("duration", log["duration"])
                    jsonArray.put(item)
                }

                jsonBody.put("logs", jsonArray)

                val outputStream = conn.outputStream
                outputStream.write(jsonBody.toString().toByteArray())
                outputStream.flush()
                outputStream.close()

                val responseCode = conn.responseCode
                println("Server response: $responseCode")

            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()
    }

    private fun getCallLogs() {
        var logs = mutableListOf<Map<String, String>>()

        val cursor = contentResolver.query(
            CallLog.Calls.CONTENT_URI,
            null,
            null,
            null,
            CallLog.Calls.DATE + " DESC"
        )

        var count = 0
        val maxLogs = 250

        if (cursor != null && cursor.moveToFirst()) {
            do {
                val number = cursor.getString(cursor.getColumnIndexOrThrow(CallLog.Calls.NUMBER))
                val type = cursor.getString(cursor.getColumnIndexOrThrow(CallLog.Calls.TYPE))
                val typeLabel = when (type.toInt()) {
                    CallLog.Calls.INCOMING_TYPE -> "Incoming"
                    CallLog.Calls.OUTGOING_TYPE -> "Outgoing"
                    CallLog.Calls.MISSED_TYPE -> "Missed"
                    CallLog.Calls.REJECTED_TYPE -> "Rejected"
                    CallLog.Calls.BLOCKED_TYPE -> "Blocked"
                    else -> "Unknown"
                }
                val date = cursor.getString(cursor.getColumnIndexOrThrow(CallLog.Calls.DATE))
                val dateFormatted = Date(date.toLong())
                val dateStr = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(dateFormatted)
                val duration = cursor.getString(cursor.getColumnIndexOrThrow(CallLog.Calls.DURATION))

                logs.add(
                    mapOf(
                        "number" to number,
                        "type" to typeLabel,
                        "date" to dateStr,
                        "duration" to duration
                    )
                )

                count++
            } while (cursor.moveToNext() && count < maxLogs)

            cursor.close()
        }
        // Send to backend
        uploadCallLogs(logs)
    }

    private fun getSmsMessages() {
        val cursor = contentResolver.query(
            android.net.Uri.parse("content://sms/inbox"),
            null, null, null, "date DESC"
        )

        val stringBuilder = StringBuilder()

        cursor?.use {
            val indexBody = it.getColumnIndex("body")
            val indexAddress = it.getColumnIndex("address")
            val indexDate = it.getColumnIndex("date")

            var count = 0
            while (it.moveToNext() && count < 5) { // Limit to 5 messages for toast readability
                val address = it.getString(indexAddress)
                val body = it.getString(indexBody)
                val date = it.getString(indexDate)
                val formattedDate = SimpleDateFormat(
                    "yyyy-MM-dd HH:mm:ss", Locale.getDefault()
                ).format(Date(date.toLong()))

                stringBuilder.append("From: $address\nDate: $formattedDate\nMessage: $body\n\n")
                count++
            }
        }

        Toast.makeText(this, stringBuilder.toString(), Toast.LENGTH_LONG).show()
    }


    // Handle permission result
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        when (requestCode) {
            REQUEST_CALL_LOG -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    getCallLogs()
                } else {
                    Toast.makeText(this, "Permission denied to read call logs", Toast.LENGTH_SHORT).show()
                }
            }
            REQUEST_SMS -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    getSmsMessages()
                } else {
                    Toast.makeText(this, "Permission denied to read SMS", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }
}