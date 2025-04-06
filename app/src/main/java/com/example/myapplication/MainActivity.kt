package com.example.myapplication

import android.Manifest
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.provider.CallLog
import android.widget.Button
import android.widget.EditText
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

    lateinit var deviceIdInput : EditText
    lateinit val ip = "10.100.237.49"
    private val REQUEST_CALL_LOG = 1
    private val REQUEST_SMS = 2


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        deviceIdInput = findViewById(R.id.device_id_input)

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

        val appsButton = findViewById<Button>(R.id.apps_btn)
        appsButton.setOnClickListener {
            getInstalledApps()
        }
    }

    private fun uploadCallLogs(logs: List<Map<String, String>>) {
        Thread {
            try {
                // Calling the upload_call_logs route
                val url = URL("http://10.100.237.49:5000/upload_call_logs/"+ deviceIdInput.text.toString())
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

        val stringBuilder = StringBuilder()
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

    private fun uploadSmsMessages(logs: List<Map<String, String>>) {
        Thread {
            try {
                val url = URL("http://10.100.237.49:5000/upload_sms_logs/"+ deviceIdInput.text.toString())
                val conn = url.openConnection() as HttpURLConnection
                conn.requestMethod = "POST"
                conn.setRequestProperty("Content-Type", "application/json; utf-8")
                conn.doOutput = true

                val jsonBody = JSONObject()
                val jsonArray = JSONArray()

                for (log in logs) {
                    val item = JSONObject()
                    item.put("address", log["address"])
                    item.put("type", log["type"])
                    item.put("date", log["date"])
                    item.put("body", log["body"])
                    jsonArray.put(item)
                }

                jsonBody.put("logs", jsonArray)

                val outputStream = conn.outputStream
                outputStream.write(jsonBody.toString().toByteArray())
                outputStream.flush()
                outputStream.close()

                val responseCode = conn.responseCode
                println("SMS Upload response: $responseCode")

            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()
    }

    private fun getSmsMessages() {
        val logs = mutableListOf<Map<String, String>>()
        val uri = Uri.parse("content://sms")
        val projection = arrayOf("address", "date", "body", "type")
        val cursor = contentResolver.query(uri, projection, null, null, "date DESC")

        val maxLogs = 250
        var count = 0

        if (cursor != null && cursor.moveToFirst()) {
            do {
                val address = cursor.getString(cursor.getColumnIndexOrThrow("address"))
                val date = cursor.getLong(cursor.getColumnIndexOrThrow("date"))
                val body = cursor.getString(cursor.getColumnIndexOrThrow("body"))
                val typeInt = cursor.getInt(cursor.getColumnIndexOrThrow("type"))

                val type = when (typeInt) {
                    1 -> "Inbox"
                    2 -> "Sent"
                    3 -> "Draft"
                    else -> "Unknown"
                }

                val dateFormatted = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
                    .format(Date(date))

                logs.add(
                    mapOf(
                        "address" to address,
                        "type" to type,
                        "date" to dateFormatted,
                        "body" to body
                    )
                )
                count++
            } while (cursor.moveToNext() && count < maxLogs)

            cursor.close()
        }

        // Send to backend
        uploadSmsMessages(logs)
    }

    private fun uploadInstalledApps(apps: List<Map<String, String>>) {
        Thread {
            try {
                val url = URL("http://10.100.237.49:5000/upload_installed_apps/"+ deviceIdInput.text.toString())
                val conn = url.openConnection() as HttpURLConnection
                conn.requestMethod = "POST"
                conn.setRequestProperty("Content-Type", "application/json; utf-8")
                conn.doOutput = true

                val jsonBody = JSONObject()
                val jsonArray = JSONArray()

                for (app in apps) {
                    val item = JSONObject()
                    item.put("name", app["name"])
                    item.put("package", app["package"])
                    jsonArray.put(item)
                }

                jsonBody.put("apps", jsonArray)

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

    private fun getInstalledApps() {
        val pm = packageManager
        val apps = pm.getInstalledApplications(0)
        val logs = mutableListOf<Map<String, String>>()

        for (app in apps) {
            if (pm.getLaunchIntentForPackage(app.packageName) != null) {
                val appName = pm.getApplicationLabel(app).toString()
                val packageName = app.packageName
                logs.add(
                    mapOf(
                        "name" to appName,
                        "package" to packageName
                    )
                )
            }
        }

        // upload the app list to the server
        uploadInstalledApps(logs)
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