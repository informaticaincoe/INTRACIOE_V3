package com.incoe.intracoe

import android.graphics.Matrix
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL

import android.view.View
import android.view.ViewGroup
import android.graphics.Canvas
import android.webkit.WebResourceError
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.util.UUID
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.net.Uri
import android.os.Bundle
import android.print.PrintAttributes
import android.print.PrintManager
import android.provider.Settings
import android.webkit.CookieManager
import android.webkit.JavascriptInterface
import android.webkit.SslErrorHandler
import android.webkit.URLUtil
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.net.http.SslError
import android.util.Log
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.annotation.RequiresApi
import androidx.annotation.RequiresPermission
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.Crossfade
import androidx.compose.animation.core.tween
import androidx.compose.animation.with
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.material3.DrawerValue
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ModalDrawerSheet
import androidx.compose.material3.ModalNavigationDrawer
import androidx.compose.material3.NavigationDrawerItem
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.rememberDrawerState
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.incoe.intracoe.ui.theme.INTRACOETheme
import kotlinx.coroutines.launch
import java.io.ByteArrayOutputStream

// ---- Preferencias de impresión ----
private const val KEY_PRINT_MODE = "print_mode"
private const val KEY_PRINTER_BT_MAC = "printer_bt_mac"
private const val KEY_PAPER_WIDTH_PX = "printer_paper_width_px"

private const val PRINT_MODE_SYSTEM = "SYSTEM"
private const val PRINT_MODE_ESC_POS_BT = "ESC_POS_BT"

private const val TAG = "BtPrint"

private const val REQ_LOC = 2001

/////////////// LISTO
fun ensureLocationPermission(activity: Activity) {
    val needFine = ContextCompat.checkSelfPermission(activity, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
    val needCoarse = ContextCompat.checkSelfPermission(activity, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED
    if (needFine || needCoarse) {
        ActivityCompat.requestPermissions(
            activity,
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION),
            REQ_LOC
        )
    }
}
fun Activity.setFullscreen(enabled: Boolean) {
    val window = this.window
    val controller = WindowInsetsControllerCompat(window, window.decorView)

    if (enabled) {
        // Dibuja por debajo de las barras y ocúltalas en modo inmersivo
        WindowCompat.setDecorFitsSystemWindows(window, false)
        controller.systemBarsBehavior =
            WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        controller.hide(WindowInsetsCompat.Type.statusBars() or WindowInsetsCompat.Type.navigationBars())
    } else {
        // Muestra de nuevo las barras del sistema
        controller.show(WindowInsetsCompat.Type.statusBars() or WindowInsetsCompat.Type.navigationBars())
        WindowCompat.setDecorFitsSystemWindows(window, true)
    }
}
///////////////////////////

///////////////// LISTO
object PrinterStore {
    fun mode(ctx: Context): String =
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .getString(KEY_PRINT_MODE, PRINT_MODE_SYSTEM) ?: PRINT_MODE_SYSTEM
    fun setMode(ctx: Context, v: String) {
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit().putString(KEY_PRINT_MODE, v).apply()
    }

    fun btMac(ctx: Context): String =
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .getString(KEY_PRINTER_BT_MAC, "00:11:22:33:44:55") ?: "00:11:22:33:44:55"

    fun paperWidthPx(ctx: Context): Int =
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .getInt(KEY_PAPER_WIDTH_PX, 576) // 576px ≈ 72/80mm a 203dpi

    fun setBt(ctx: Context, mac: String, paperWidthPx: Int = 576) {
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit()
            .putString(KEY_PRINTER_BT_MAC, mac)
            .putInt(KEY_PAPER_WIDTH_PX, paperWidthPx)
            .apply()
    }
}
////////////////////

///////////////// LISTO
fun hasScanPermission(ctx: Context): Boolean {
    return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        ContextCompat.checkSelfPermission(ctx, Manifest.permission.BLUETOOTH_SCAN) == PackageManager.PERMISSION_GRANTED
    } else {
        ContextCompat.checkSelfPermission(ctx, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
    }
}

fun requestScanPermission(activity: Activity) {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        ActivityCompat.requestPermissions(activity, arrayOf(Manifest.permission.BLUETOOTH_SCAN), 1002)
    } else {
        ActivityCompat.requestPermissions(activity, arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), 1003)
    }
}

fun hasConnectPermission(ctx: Context): Boolean {
    return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        ContextCompat.checkSelfPermission(ctx, Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED
    } else true
}

///////////////////////

///////////// LISTO
/* -------------------- Constantes -------------------- */
private const val PREFS = "intracoe_prefs"
private const val KEY_URL = "server_url"
private const val KEY_LOGGED_IN = "logged_in"

/* -------------------- Rutas -------------------- */
sealed class Route(val route: String) {
    data object Home : Route("home")
    data object Settings : Route("settings")
}

/* -------------------- Preferencias -------------------- */
object ServerUrlStore {
    fun get(ctx: Context): String =
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .getString(KEY_URL, "https://intracoe.incoe.cloud/") ?: "https://intracoe.incoe.cloud/"
    fun set(ctx: Context, value: String) {
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit().putString(KEY_URL, value).apply()
    }
}

object SessionStore {
    fun isLoggedIn(ctx: Context): Boolean =
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getBoolean(KEY_LOGGED_IN, false)
    fun setLoggedIn(ctx: Context, value: Boolean) {
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit().putBoolean(KEY_LOGGED_IN, value).apply()
    }
}

/* -------------------- Helpers sesión / URL / Red -------------------- */
private val SESSION_COOKIE_CANDIDATES = listOf("sessionid", "session_id", "odoo_session", "auth_token")

private fun originOf(url: String): String {
    val u = Uri.parse(url)
    val port = if (u.port != -1) ":${u.port}" else ""
    return "${u.scheme}://${u.host}$port"
}

private fun absolutizeUrl(base: String, raw: String): String {
    if (URLUtil.isNetworkUrl(raw)) return raw
    val baseOrigin = originOf(base)
    return when {
        raw.startsWith("/") -> baseOrigin + raw
        raw.startsWith("file://") -> baseOrigin + "/" + raw.removePrefix("file://").trimStart('/')
        else -> if (base.endsWith("/")) base + raw.trimStart('/') else "$base/$raw"
    }
}

private fun hasSessionCookie(serverUrl: String): Boolean {
    val cm = CookieManager.getInstance()
    val cookies = cm.getCookie(serverUrl) ?: cm.getCookie(originOf(serverUrl)) ?: return false
    return SESSION_COOKIE_CANDIDATES.any { cookies.contains("$it=") }
}

private fun isNetworkAvailable(ctx: Context): Boolean {
    val cm = ctx.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    val nw = cm.activeNetwork ?: return false
    val caps = cm.getNetworkCapabilities(nw) ?: return false
    return caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
}

/* -------------------- Modelos de error -------------------- */
sealed class WebErrorType {
    data object InvalidUrl : WebErrorType()
    data object NoInternet : WebErrorType()
    data class Http(val code: Int) : WebErrorType()
    data object Ssl : WebErrorType()
    data object Timeout : WebErrorType()
    data object Connection : WebErrorType()
    data object Unknown : WebErrorType()
}
data class WebError(val type: WebErrorType, val detail: String? = null)

/* -------------------- Activity -------------------- */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        ensureLocationPermission(this)   // 👈 pide permiso de ubicación
        android.webkit.WebView.setWebContentsDebuggingEnabled(true) // 👈
        enableEdgeToEdge()
        setContent { INTRACOEApp() }
    }
}

///////////////////////////////////////////

/////////////////// listo
/* -------------------- App UI -------------------- */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun INTRACOEApp() {

    INTRACOETheme {

        val ctx = LocalContext.current
        val activity = ctx as? Activity                     // 👈 necesitas la Activity
        var serverUrl by remember { mutableStateOf(ServerUrlStore.get(ctx)) }
        var loggedIn by remember { mutableStateOf(SessionStore.isLoggedIn(ctx)) }
        var reloadTrigger by remember { mutableStateOf(0) }

        // 1) Chequeo inicial por cookies (por si ya trae sesión)
        LaunchedEffect(serverUrl) {
            val cookieLogin = hasSessionCookie(serverUrl)
            if (cookieLogin != loggedIn) {
                loggedIn = cookieLogin
                SessionStore.setLoggedIn(ctx, cookieLogin)
            }
        }

        // 2) Ocultar/mostrar barras del sistema según login
        LaunchedEffect(loggedIn) {                          // 👈 aquí, no en serverUrl
            activity?.setFullscreen(loggedIn)
        }

        Crossfade(targetState = loggedIn, animationSpec = tween(150)) { isLogged ->
            if (isLogged) {
                // ===== LOGUEADO → SOLO WEBVIEW =====
                HomeScreen(
                    serverUrl = serverUrl,
                    reloadTrigger = 0,
                    onLoginDetected = {
                        if (!SessionStore.isLoggedIn(ctx)) SessionStore.setLoggedIn(ctx, true)
                        if (!loggedIn) loggedIn = true
                    },
                    onLogoutDetected = {
                        SessionStore.setLoggedIn(ctx, false)
                        loggedIn = false
                    },
                    onChangeServerUrl = { newUrl ->
                        ServerUrlStore.set(ctx, newUrl)
                        serverUrl = newUrl
                    }
                )
            } else  {
                // ===== NO LOGUEADO → MENÚ + TOPBAR + WEBVIEW =====
                val nav = rememberNavController()
                val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
                val scope = rememberCoroutineScope()

                ModalNavigationDrawer(
                    drawerState = drawerState,
                    drawerContent = {
                        ModalDrawerSheet {
                            Spacer(Modifier.height(8.dp))
                            Text("Menú", modifier = Modifier.padding(horizontal = 16.dp))
                            Spacer(Modifier.height(8.dp))
                            NavigationDrawerItem(
                                label = { Text("Inicio") },
                                selected = true,
                                onClick = { scope.launch { drawerState.close() } }
                            )
                            NavigationDrawerItem(
                                label = { Text("Configuración") },
                                selected = false,
                                onClick = {
                                    scope.launch { drawerState.close() }
                                    nav.navigate(Route.Settings.route)
                                }
                            )
                        }
                    }
                ) {
                    Scaffold(
                        topBar = {
                            TopAppBar(
                                title = { Text("INTRACOE") },
                                navigationIcon = {
                                    IconButton(onClick = { scope.launch { drawerState.open() } }) {
                                        Icon(Icons.Default.Menu, contentDescription = "Menú")
                                    }
                                },
                                actions = {
                                    IconButton(onClick = { reloadTrigger++ }) {
                                        Icon(Icons.Default.Refresh, contentDescription = "Actualizar")
                                    }
                                }
                            )
                        }
                    ) { inner ->
                        NavHost(
                            navController = nav,
                            startDestination = Route.Home.route,
                            modifier = Modifier.padding(inner)
                        ) {
                            composable(Route.Home.route) {
                                HomeScreen(
                                    serverUrl = serverUrl,
                                    reloadTrigger = reloadTrigger,
                                    onLoginDetected = {
                                        SessionStore.setLoggedIn(ctx, true); loggedIn = true
                                    },
                                    onLogoutDetected = {
                                        SessionStore.setLoggedIn(ctx, false); loggedIn = false
                                    },
                                    onChangeServerUrl = { newUrl ->
                                        ServerUrlStore.set(ctx, newUrl); serverUrl = newUrl
                                    }
                                )
                            }
                            composable(Route.Settings.route) {
                                SettingsScreen(
                                    current = serverUrl,
                                    onSaved = {
                                        ServerUrlStore.set(ctx, it)
                                        serverUrl = it
                                        nav.popBackStack()
                                    }
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

//////////////////////////////////////////////////////


/////////////////// listo
/* -------------------- Puente JS para impresión -------------------- */
class WebAppPrinter(
    private val activity: Activity,
    private val baseUrl: String
) {
    @JavascriptInterface
    fun printFactura(rawUrl: String) {
        Log.d("AndroidPrinter", "printFactura URL: $rawUrl")
        activity.runOnUiThread {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val ok = ContextCompat.checkSelfPermission(activity, Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED
                if (!ok) {
                    Toast.makeText(activity, "Concede permiso Bluetooth y vuelve a tocar Imprimir", Toast.LENGTH_SHORT).show()
                    ActivityCompat.requestPermissions(activity, arrayOf(Manifest.permission.BLUETOOTH_CONNECT), 1001)
                    return@runOnUiThread
                }
            }
            Log.d(TAG, "printFactura rawUrl=$rawUrl base=$baseUrl")
            val normalized = absolutizeUrl(baseUrl, rawUrl)
            val mode = PrinterStore.mode(activity)
            val mac  = PrinterStore.btMac(activity)
            val wpx  = PrinterStore.paperWidthPx(activity)
            Log.d(TAG, "printFactura normalized=$normalized mode=$mode mac=$mac widthPx=$wpx")
            when (PrinterStore.mode(activity)) {
                PRINT_MODE_ESC_POS_BT -> {
                    // (En Android 12+ asegúrate de tener el permiso antes)
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                        val ok = ContextCompat.checkSelfPermission(activity, Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED
                        if (!ok) {
                            ActivityCompat.requestPermissions(activity, arrayOf(Manifest.permission.BLUETOOTH_CONNECT), 1001)
                            return@runOnUiThread
                        }
                    }
                    SilentEscPosBt.printUrlSilently(
                        ctx = activity,
                        url = normalized,
                        mac = PrinterStore.btMac(activity),
                        paperWidthPx = PrinterStore.paperWidthPx(activity)
                    )
                }
                else -> {
                    // Modo sistema (diálogo PrintManager)
                    val wv = WebView(activity)
                    with(wv.settings) {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        loadsImagesAutomatically = true
                        allowFileAccess = false
                        allowContentAccess = true
                    }
                    wv.webViewClient = object : WebViewClient() {
                        override fun onPageFinished(view: WebView?, urlFinished: String?) {
                            val pm = activity.getSystemService(Activity.PRINT_SERVICE) as PrintManager
                            pm.print(
                                "Factura INTRACOE",
                                wv.createPrintDocumentAdapter("Factura_INTRACOE"),
                                PrintAttributes.Builder()
                                    .setMinMargins(PrintAttributes.Margins.NO_MARGINS)
                                    .setMediaSize(PrintAttributes.MediaSize.UNKNOWN_PORTRAIT)
                                    .build()
                            )
                        }
                    }
                    wv.loadUrl(normalized)
                }
            }
        }
    }
}

//////////////////////////////////////////////////////


/* -------------------- HOME: WebView + manejo de errores -------------------- */
@Composable
fun HomeScreen(
    serverUrl: String,
    reloadTrigger: Int = 0,
    onLoginDetected: () -> Unit = {},
    onLogoutDetected: () -> Unit = {},
    onChangeServerUrl: (String) -> Unit = {}
) {
    val context = LocalContext.current
    val activity = context as? Activity

    var progress by remember { mutableStateOf(0) }
    var canGoBack by remember { mutableStateOf(false) }
    var webViewRef by remember { mutableStateOf<WebView?>(null) }
    var webError by remember { mutableStateOf<WebError?>(null) }
    var showEditUrl by remember { mutableStateOf(false) }

    BackHandler(enabled = canGoBack) { webViewRef?.goBack() }

    // Trigger de recarga
    LaunchedEffect(reloadTrigger) {
        webError = null
        webViewRef?.reload()
    }

    // Validación inicial de URL / Conectividad
    LaunchedEffect(serverUrl) {
        webError = when {
            !URLUtil.isNetworkUrl(serverUrl) -> WebError(WebErrorType.InvalidUrl, "La URL no es válida.")
            !isNetworkAvailable(context) -> WebError(WebErrorType.NoInternet, "No hay conexión a internet.")
            else -> null
        }
    }

    Column {
        // Progreso
        if (webError == null && progress in 1..99) {
            LinearProgressIndicator(progress = progress / 100f, modifier = Modifier.fillMaxWidth())
        }

        Box(Modifier.fillMaxSize()) {

            // ============ WebView ============
            if (webError == null) {
                AndroidView(
                    modifier = Modifier.fillMaxSize(),
                    factory = { ctx ->
                        WebView(ctx).apply {
                            settings.javaScriptEnabled = true
                            settings.domStorageEnabled = true
                            settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                            settings.useWideViewPort = true
                            settings.loadWithOverviewMode = true
                            settings.builtInZoomControls = false
                            settings.displayZoomControls = false
                            settings.loadsImagesAutomatically = true
                            settings.allowFileAccess = true
                            settings.allowContentAccess = true
                            // 👇 Habilitar geolocalización para WebView
                            settings.setGeolocationEnabled(true)

                            CookieManager.getInstance().setAcceptCookie(true)
                            CookieManager.getInstance().setAcceptThirdPartyCookies(this, true)

                            // Puente impresión (con baseUrl para normalizar)
                            activity?.let { addJavascriptInterface(WebAppPrinter(it, serverUrl), "AndroidPrinter") }

                            webViewClient = object : WebViewClient() {

                                private fun updateAuthState(url: String?) {
                                    val cookieLogin = hasSessionCookie(serverUrl)

                                    val looksLikeLogin = url?.let {
                                        it.contains("login", ignoreCase = true) ||
                                                it.contains("/accounts/", ignoreCase = true) ||
                                                it.contains("/web/login", ignoreCase = true)
                                    } == true

                                    val looksLikeLogout = url?.contains("logout", ignoreCase = true) == true

                                    when {
                                        cookieLogin && !looksLikeLogin -> onLoginDetected()
                                        looksLikeLogout || (!cookieLogin && looksLikeLogin) -> onLogoutDetected()
                                        else -> {
                                            // Fallback por DOM
                                            evaluateJavascript(
                                                "(function(){try{return !!(document.querySelector('a[href*=\"logout\"],form[action*=\"logout\"]'));}catch(e){return false;}})();"
                                            ) { hasLogout ->
                                                if (hasLogout == "true") onLoginDetected() else onLogoutDetected()
                                            }
                                        }
                                    }
                                }

                                override fun shouldOverrideUrlLoading(
                                    view: WebView, request: WebResourceRequest
                                ): Boolean {
                                    val u = request.url.toString()
                                    return when {
                                        u.startsWith("tel:") || u.startsWith("mailto:") || u.startsWith("whatsapp:") -> {
                                            try { ctx.startActivity(Intent(Intent.ACTION_VIEW, request.url)) } catch (_: Exception) {}
                                            true
                                        }
                                        // 👉 abre Maps/geo fuera del WebView
                                        u.contains("google.com/maps") || u.startsWith("geo:") || u.startsWith("https://maps.app.goo.gl") -> {
                                            try { view.context.startActivity(Intent(Intent.ACTION_VIEW, request.url)) } catch (_: Exception) {}
                                            true
                                        }
                                        URLUtil.isNetworkUrl(u) -> false
                                        else -> {
                                            webError = WebError(WebErrorType.InvalidUrl, "Esquema no soportado: $u")
                                            true
                                        }
                                    }
                                }

                                override fun onPageStarted(view: WebView, url: String?, favicon: Bitmap?) {
                                    canGoBack = view.canGoBack()
                                }

                                override fun onPageFinished(view: WebView, url: String?) {
                                    canGoBack = view.canGoBack()
                                    // Si terminó sin errores previos, limpiar estado de error
                                    if (webError == null) updateAuthState(url)
                                }

                                override fun onReceivedHttpError(
                                    view: WebView,
                                    request: WebResourceRequest,
                                    errorResponse: WebResourceResponse
                                ) {
                                    if (request.isForMainFrame) {
                                        webError = WebError(WebErrorType.Http(errorResponse.statusCode), "HTTP ${errorResponse.statusCode}")
                                    }
                                }

                                override fun onReceivedError(
                                    view: WebView,
                                    request: WebResourceRequest,
                                    error: android.webkit.WebResourceError
                                ) {
                                    if (!request.isForMainFrame) return
                                    val type = when (error.errorCode) {
                                        WebViewClient.ERROR_CONNECT,
                                        WebViewClient.ERROR_HOST_LOOKUP,
                                        WebViewClient.ERROR_UNKNOWN -> WebErrorType.Connection
                                        WebViewClient.ERROR_TIMEOUT -> WebErrorType.Timeout
                                        else -> WebErrorType.Unknown
                                    }
                                    webError = WebError(type, error.description?.toString())
                                }

                                override fun onReceivedSslError(
                                    view: WebView,
                                    handler: SslErrorHandler,
                                    error: SslError
                                ) {
                                    handler.cancel()
                                    webError = WebError(WebErrorType.Ssl, "Error SSL: ${error.primaryError}")
                                }
                            }

                            webChromeClient = object : WebChromeClient() {
                                override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                    progress = newProgress
                                }
                                override fun onCreateWindow(view: WebView, isDialog: Boolean, isUserGesture: Boolean, resultMsg: android.os.Message): Boolean {
                                    val transport = resultMsg.obj as WebView.WebViewTransport
                                    transport.webView = view
                                    resultMsg.sendToTarget()
                                    return true
                                }
                                override fun onGeolocationPermissionsShowPrompt(
                                    origin: String?,
                                    callback: android.webkit.GeolocationPermissions.Callback?
                                ) {
                                    // concede geolocalización al sitio que lo pida
                                    callback?.invoke(origin, true, false)
                                }
                            }

                            setDownloadListener { dlUrl, _, _, _, _ ->
                                try { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(dlUrl))) } catch (_: Exception) {}
                            }

                            // Cargar o mostrar error previo de conectividad/URL
                            when {
                                !URLUtil.isNetworkUrl(serverUrl) ->
                                    webError = WebError(WebErrorType.InvalidUrl, "La URL no es válida.")
                                !isNetworkAvailable(ctx) ->
                                    webError = WebError(WebErrorType.NoInternet, "No hay conexión a internet.")
                                else -> loadUrl(serverUrl)
                            }

                            webViewRef = this
                        }
                    },
                    update = { wv ->
                        if (webError == null && wv.url?.startsWith(serverUrl) != true) {
                            wv.loadUrl(serverUrl)
                        }
                    }
                )
            }

            // ============ Pantalla de Error ============
            webError?.let { err ->
                ErrorScreen(
                    error = err,
                    currentUrl = serverUrl,
                    onRetry = {
                        webError = when {
                            !URLUtil.isNetworkUrl(serverUrl) -> WebError(WebErrorType.InvalidUrl, "La URL no es válida.")
                            !isNetworkAvailable(context) -> WebError(WebErrorType.NoInternet, "No hay conexión a internet.")
                            else -> null
                        }
                        if (webError == null) webViewRef?.reload()
                    },
                    onEditUrl = { showEditUrl = true },
                    onOpenWifi = {
                        runCatching {
                            context.startActivity(Intent(Settings.ACTION_WIFI_SETTINGS))
                        }
                    }
                )
            }

            if (showEditUrl) {
                EditUrlDialog(
                    initial = serverUrl,
                    onDismiss = { showEditUrl = false },
                    onSave = { newUrl ->
                        onChangeServerUrl(newUrl)
                        showEditUrl = false
                        webError = null
                        webViewRef?.loadUrl(newUrl)
                    }
                )
            }
        }
    }
}

/* -------------------- Pantallas auxiliares -------------------- */
@Composable
fun ErrorScreen(
    error: WebError,
    currentUrl: String,
    onRetry: () -> Unit,
    onEditUrl: () -> Unit,
    onOpenWifi: () -> Unit
) {
    val (title, subtitle) = when (val t = error.type) {
        is WebErrorType.InvalidUrl -> "URL inválida" to "Revisa que sea una URL con https://\nActual: $currentUrl"
        is WebErrorType.NoInternet -> "Sin conexión" to "Conéctate a una red Wi-Fi o datos móviles."
        is WebErrorType.Http -> "Error del servidor (${t.code})" to (error.detail ?: "No se pudo cargar la página.")
        is WebErrorType.Ssl -> "Error de seguridad (SSL)" to (error.detail ?: "Conexión no segura.")
        is WebErrorType.Timeout -> "Tiempo de espera agotado" to "La página tardó demasiado en responder."
        is WebErrorType.Connection -> "No se pudo conectar" to (error.detail ?: "Verifica tu red.")
        is WebErrorType.Unknown -> "Error desconocido" to (error.detail ?: "Inténtalo de nuevo.")
    }

    Surface(Modifier.fillMaxSize()) {
        Column(
            Modifier
                .fillMaxSize()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(title, style = MaterialTheme.typography.headlineSmall)
            Spacer(Modifier.height(8.dp))
            Text(subtitle, style = MaterialTheme.typography.bodyMedium)
            Spacer(Modifier.height(20.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Button(onClick = onRetry) { Text("Reintentar") }
                OutlinedButton(onClick = onEditUrl) { Text("Editar URL") }
                OutlinedButton(onClick = onOpenWifi) { Text("Abrir Wi-Fi") }
            }
        }
    }
}

@Composable
fun EditUrlDialog(
    initial: String,
    onDismiss: () -> Unit,
    onSave: (String) -> Unit
) {
    var field by remember(initial) { mutableStateOf(TextFieldValue(initial)) }
    var error by remember { mutableStateOf<String?>(null) }

    AlertDialog(
        onDismissRequest = onDismiss,
        confirmButton = {
            Button(onClick = {
                val raw = field.text.trim()
                if (!URLUtil.isNetworkUrl(raw)) {
                    error = "URL inválida. Ej: https://intracoe.incoe.cloud/"
                    return@Button
                }
                onSave(raw)
            }) { Text("Guardar") }
        },
        dismissButton = {
            OutlinedButton(onClick = onDismiss) { Text("Cancelar") }
        },
        title = { Text("Editar URL del servidor") },
        text = {
            Column {
                OutlinedTextField(
                    value = field,
                    onValueChange = { field = it; error = null },
                    label = { Text("URL") },
                    placeholder = { Text("https://intracoe.incoe.cloud/") },
                    singleLine = true,
                    isError = error != null,
                    supportingText = { if (error != null) Text(error!!, color = MaterialTheme.colorScheme.error) }
                )
            }
        }
    )
}

/* -------------------- SETTINGS -------------------- */
@Composable
fun SettingsScreen(current: String, onSaved: (String) -> Unit) {
    var field by remember(current) { mutableStateOf(TextFieldValue(current)) }
    var error by remember { mutableStateOf<String?>(null) }

    Column(Modifier.padding(16.dp)) {
        Text("Configuración del servidor", style = MaterialTheme.typography.titleLarge)
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = field,
            onValueChange = { field = it; error = null },
            label = { Text("URL de la app web") },
            placeholder = { Text("https://intracoe.incoe.cloud/") },
            singleLine = true,
            isError = error != null,
            supportingText = { if (error != null) Text(error!!, color = MaterialTheme.colorScheme.error) }
        )
        Spacer(Modifier.height(12.dp))
        Button(onClick = {
            val raw = field.text.trim()
            if (!URLUtil.isNetworkUrl(raw)) {
                error = "URL inválida. Ej: https://intracoe.incoe.cloud/"
                return@Button
            }
            onSaved(raw)
        }) {
            Text("Guardar")
        }
        Divider(Modifier.padding(vertical = 16.dp))
        PrinterSettingsSectionWithScan()   // 👈 AQUI se integra la config + escaneo
    }
}

@Composable
fun PrinterSettingsSectionWithScan() {
    val ctx = LocalContext.current
    val activity = (ctx as? Activity) ?: return   // evita crash en Preview
    val adapter = remember { BluetoothAdapter.getDefaultAdapter() }

    var silent by remember { mutableStateOf(PrinterStore.mode(ctx) == PRINT_MODE_ESC_POS_BT) }
    var mac by remember { mutableStateOf(PrinterStore.btMac(ctx)) }
    var width by remember { mutableStateOf(PrinterStore.paperWidthPx(ctx).toString()) }

    var scanning by remember { mutableStateOf(false) }
    val discovered = remember { mutableStateListOf<BluetoothDevice>() }

    // ⚠️ NUNCA leas bondedDevices sin permiso en Android 12+ → SecurityException
    val paired by remember {
        mutableStateOf(
            if (adapter == null) emptyList()
            else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S &&
                ContextCompat.checkSelfPermission(ctx, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED
            ) emptyList()
            else runCatching { adapter.bondedDevices?.toList().orEmpty() }.getOrDefault(emptyList())
        )
    }

    // Receiver + discovery controlado por permisos
    DisposableEffect(scanning) {
        if (!scanning) return@DisposableEffect onDispose { }

        if (!hasScanPermission(ctx)) {
            scanning = false
            return@DisposableEffect onDispose { }
        }

        val receiver = object : android.content.BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                when (intent.action) {
                    BluetoothDevice.ACTION_FOUND -> {
                        val dev: BluetoothDevice? = if (Build.VERSION.SDK_INT >= 33) {
                            intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE, BluetoothDevice::class.java)
                        } else {
                            @Suppress("DEPRECATION")
                            intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE) as? BluetoothDevice
                        }
                        dev?.let {
                            if (discovered.none { it.address == dev.address }) discovered += dev
                        }
                    }
                    BluetoothAdapter.ACTION_DISCOVERY_FINISHED -> scanning = false
                }
            }
        }

        val filter = android.content.IntentFilter().apply {
            addAction(BluetoothDevice.ACTION_FOUND)
            addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED)
        }

        ctx.registerReceiver(receiver, filter)

        // Inicia escaneo (protegido)
        try {
            if (adapter?.isEnabled == true) {
                @SuppressLint("MissingPermission")
                adapter.startDiscovery()
            } else scanning = false
        } catch (_: SecurityException) {
            scanning = false
        }

        onDispose {
            runCatching { ctx.unregisterReceiver(receiver) }
            try {
                @SuppressLint("MissingPermission")
                adapter?.cancelDiscovery()
            } catch (_: SecurityException) { /* no-op */ }
        }
    }

    Spacer(Modifier.height(24.dp))
    Text("Impresora", style = MaterialTheme.typography.titleMedium)
    Spacer(Modifier.height(8.dp))

    if (adapter == null) {
        Text("Este dispositivo no tiene Bluetooth.", color = MaterialTheme.colorScheme.error)
        return
    }

    Row(verticalAlignment = Alignment.CenterVertically) {
        Switch(
            checked = silent,
            onCheckedChange = {
                silent = it
                PrinterStore.setMode(ctx, if (it) PRINT_MODE_ESC_POS_BT else PRINT_MODE_SYSTEM)
            }
        )
        Spacer(Modifier.width(8.dp))
        Text(if (silent) "Impresión silenciosa (Bluetooth)" else "Impresión del sistema")
    }
    Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        OutlinedButton(onClick = {
            SilentEscPosBt.printTextTest(ctx, PrinterStore.btMac(ctx))
        }) { Text("Probar texto") }

        OutlinedButton(onClick = {
            SilentEscPosBt.printHtmlSilently(
                ctx = ctx,
                html = """
           <html><body style="width:${PrinterStore.paperWidthPx(ctx)}px;font:14px monospace">
             <h3 style="text-align:center;margin:6px 0">Prueba de imagen</h3>
             <div style="border:1px solid #000;padding:8px;margin:6px 0">
               Caja, texto, líneas y <b>acentos</b> áéíóú ñ ✓
             </div>
             <img src="https://upload.wikimedia.org/wikipedia/commons/3/3a/LogoAndroid.png" style="width:100%">
           </body></html>
        """.trimIndent(),
                mac = PrinterStore.btMac(ctx),
                paperWidthPx = PrinterStore.paperWidthPx(ctx)
            )
        }) { Text("Probar imagen") }

        OutlinedButton(onClick = {
            SilentEscPosBt.printPdfSilently(
                ctx = ctx,
                url = "https://intracoe.incoe.cloud/fe/factura_pdf/76/",  // tu PDF real
                mac = PrinterStore.btMac(ctx),
                paperWidthPx = PrinterStore.paperWidthPx(ctx)
            )
        }) { Text("Probar PDF") }
    }

    Spacer(Modifier.height(8.dp))
    OutlinedTextField(
        value = mac,
        onValueChange = { mac = it },
        label = { Text("MAC RPP300 (emparejada)") },
        singleLine = true
    )
    Spacer(Modifier.height(8.dp))
    OutlinedTextField(
        value = width,
        onValueChange = { width = it.filter(Char::isDigit) },
        label = { Text("Ancho (px)") },
        singleLine = true
    )
    Spacer(Modifier.height(8.dp))
    Button(onClick = {
        PrinterStore.setBt(ctx, mac, width.toIntOrNull() ?: 576)
        // Pedir BLUETOOTH_CONNECT en Android 12+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S &&
            ContextCompat.checkSelfPermission(ctx, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(activity, arrayOf(Manifest.permission.BLUETOOTH_CONNECT), 1001)
        }
    }) { Text("Guardar impresora") }

    Spacer(Modifier.height(16.dp))
    Text("Dispositivos emparejados", style = MaterialTheme.typography.titleSmall)
    if (paired.isEmpty()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("No hay dispositivos emparejados.")
            Spacer(Modifier.width(8.dp))
            OutlinedButton(onClick = {
                ctx.startActivity(Intent(Settings.ACTION_BLUETOOTH_SETTINGS))
            }) { Text("Abrir Bluetooth") }
        }
    } else {
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            paired.forEach { dev ->
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        // Nombre puede requerir CONNECT; si no hay permiso, muestra solo la MAC
                        val hasConnect = Build.VERSION.SDK_INT < Build.VERSION_CODES.S ||
                                ContextCompat.checkSelfPermission(ctx, Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED
                        Text(if (hasConnect) (dev.name ?: "(sin nombre)") else "(sin permiso para nombre)")
                        Text(dev.address, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    OutlinedButton(onClick = {
                        mac = dev.address
                        PrinterStore.setBt(ctx, mac, width.toIntOrNull() ?: 576)
                    }) { Text("Usar") }
                }
            }
        }
    }

    Spacer(Modifier.height(16.dp))
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text("Buscar nuevos", style = MaterialTheme.typography.titleSmall, modifier = Modifier.weight(1f))
        if (!scanning) {
            OutlinedButton(onClick = {
                // Pedir permisos de escaneo
                if (!hasScanPermission(ctx)) {
                    requestScanPermission(activity)
                    return@OutlinedButton
                }
                if (adapter.isEnabled != true) {
                    ctx.startActivity(Intent(Settings.ACTION_BLUETOOTH_SETTINGS))
                    return@OutlinedButton
                }
                discovered.clear()
                scanning = true
                try {
                    @SuppressLint("MissingPermission")
                    adapter.startDiscovery()
                } catch (_: SecurityException) {
                    scanning = false
                }
            }) { Text("Escanear") }
        } else {
            CircularProgressIndicator(modifier = Modifier.size(20.dp))
            Spacer(Modifier.width(8.dp))
            Text("Escaneando…")
            Spacer(Modifier.width(8.dp))
            OutlinedButton(onClick = {
                scanning = false
                try {
                    @SuppressLint("MissingPermission")
                    adapter.cancelDiscovery()
                } catch (_: SecurityException) { }
            }) { Text("Detener") }
        }
    }

    if (discovered.isNotEmpty()) {
        Spacer(Modifier.height(8.dp))
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            discovered.forEach { dev ->
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        val hasConnect = Build.VERSION.SDK_INT < Build.VERSION_CODES.S ||
                                ContextCompat.checkSelfPermission(ctx, Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED
                        Text(if (hasConnect) (dev.name ?: "(sin nombre)") else "(sin permiso para nombre)")
                        Text(dev.address, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    OutlinedButton(onClick = {
                        mac = dev.address
                        PrinterStore.setBt(ctx, mac, width.toIntOrNull() ?: 576)
                    }) { Text("Usar") }
                }
            }
        }
    }
}

/* -------------------- PREVIEW -------------------- */
@Preview(showBackground = true)
@Composable
fun SettingsPreview() {
    INTRACOETheme {
        SettingsScreen(current = "https://intracoe.incoe.cloud/", onSaved = {})
    }
}

/* -------------------- Impresión ESC/POS silenciosa por Bluetooth -------------------- */
object SilentEscPosBt {
    private val SPP_UUID: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")

    fun printPdfSilently(ctx: Context, url: String, mac: String, paperWidthPx: Int = 576) {
        Thread {
            try {
                Log.d(TAG, "Descargando PDF: $url")
                val conn = (URL(url).openConnection() as HttpURLConnection).apply {
                    CookieManager.getInstance().getCookie(url)?.let { setRequestProperty("Cookie", it) }
                }
                val code = conn.responseCode
                val len = conn.contentLength
                Log.d(TAG, "HTTP $code length=$len")
                val pdfFile = File(ctx.cacheDir, "tmp_factura.pdf")
                conn.inputStream.use { input -> FileOutputStream(pdfFile).use { input.copyTo(it) } }
                Log.d(TAG, "PDF guardado en: ${pdfFile.absolutePath} (${pdfFile.length()} bytes)")

                val pfd = ParcelFileDescriptor.open(pdfFile, ParcelFileDescriptor.MODE_READ_ONLY)
                val renderer = PdfRenderer(pfd)
                if (renderer.pageCount == 0) { Log.e(TAG, "PDF sin páginas"); return@Thread }
                val page = renderer.openPage(0)

                val scale = paperWidthPx.toFloat() / page.width
                val bmp = Bitmap.createBitmap(paperWidthPx, (page.height * scale).toInt(), Bitmap.Config.ARGB_8888)
                val m = Matrix().apply { setScale(scale, scale) }
                page.render(bmp, null, m, PdfRenderer.Page.RENDER_MODE_FOR_PRINT)
                page.close(); renderer.close(); pfd.close()
                try {
                    val f = File(ctx.cacheDir, "last_bitmap_pdf.png")
                    FileOutputStream(f).use { bmp.compress(Bitmap.CompressFormat.PNG, 100, it) }
                    Log.d(TAG, "Bitmap PDF guardado en: ${f.absolutePath} (${bmp.width}x${bmp.height})")
                } catch (e: Exception) { /* ignore */ }

                Log.d(TAG, "Enviando bitmap de PDF a impresora…")
                sendBitmapEscPosOverBt(ctx, mac, bmp)
            } catch (e: Exception) {
                Log.e(TAG, "printPdfSilently error", e)
            }
        }.start()
    }

    fun printHtmlSilently(ctx: Context, html: String, mac: String, paperWidthPx: Int = 576) {
        renderHtmlToBitmap(ctx, html, paperWidthPx) { bmp, err ->
            if (bmp != null) Thread { runCatching { sendBitmapEscPosOverBt(ctx, mac, bmp) } }.start()
        }
    }

    private fun renderHtmlToBitmap(
        ctx: Context,
        html: String,
        widthPx: Int,
        callback: (Bitmap?, Throwable?) -> Unit
    ) {
        Log.d(TAG, "renderHtmlToBitmap: widthPx=$widthPx")
        val wv = WebView(ctx)
        with(wv.settings) {
            javaScriptEnabled = true
            domStorageEnabled = true
            useWideViewPort = true
            loadWithOverviewMode = true
            mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
            blockNetworkImage = false
        }
        wv.layoutParams = ViewGroup.LayoutParams(widthPx, ViewGroup.LayoutParams.WRAP_CONTENT)

        fun drawWithHeightPx(view: WebView, heightPx: Int) {
            val h = heightPx.coerceAtLeast(1)
            val wSpec = View.MeasureSpec.makeMeasureSpec(widthPx, View.MeasureSpec.EXACTLY)
            val hSpec = View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED)
            view.measure(wSpec, hSpec)
            view.layout(0, 0, widthPx, h)
            val bmp = Bitmap.createBitmap(widthPx, h, Bitmap.Config.ARGB_8888)
            Canvas(bmp).apply { view.draw(this) }
            try {
                val f = File(ctx.cacheDir, "last_bitmap_html.png")
                FileOutputStream(f).use { bmp.compress(Bitmap.CompressFormat.PNG, 100, it) }
                Log.d(TAG, "Bitmap HTML guardado: ${f.absolutePath} (${bmp.width}x${bmp.height})")
            } catch (_: Exception) { }
            callback(bmp, null)
        }

        fun measureAndDraw(view: WebView, attempt: Int = 0) {
            // 1) scrollHeight en CSS px
            view.evaluateJavascript(
                "(function(){var d=document;var h=Math.max(d.body?d.body.scrollHeight:0,d.documentElement?d.documentElement.scrollHeight:0);return h;})()"
            ) { cssHStr ->
                val cssH = cssHStr?.replace("\"", "")?.toFloatOrNull() ?: 0f
                val pxByScale = (cssH * view.scale).toInt()
                val pxByDp = (cssH * ctx.resources.displayMetrics.density).toInt()
                val ch = (view.contentHeight * view.scale).toInt()
                val best = listOf(pxByScale, pxByDp, ch).maxOrNull() ?: 0

                Log.d(TAG, "measure: cssH=$cssH scale=${view.scale} → pxByScale=$pxByScale pxByDp=$pxByDp contentPx=$ch best=$best attempt=$attempt")

                if (best > 1) {
                    drawWithHeightPx(view, best)
                } else if (attempt < 10) {
                    // espera un poco (imágenes / fuentes)
                    view.postDelayed({ measureAndDraw(view, attempt + 1) }, 150)
                } else {
                    callback(null, Exception("Nada que renderizar (height=0)"))
                }
            }
        }

        wv.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView, url: String?) {
                Log.d(TAG, "HTML onPageFinished; contentHeight=${view.contentHeight} scale=${view.scale}")
                // Espera a que las imágenes terminen
                fun waitImages(attempt: Int = 0) {
                    view.evaluateJavascript(
                        "(function(){try{var a=[].slice.call(document.images);return a.length===0||a.every(i=>i.complete);}catch(e){return true}})();"
                    ) { all ->
                        val ok = all == "true"
                        if (ok) measureAndDraw(view)
                        else if (attempt < 10) view.postDelayed({ waitImages(attempt + 1) }, 120)
                        else measureAndDraw(view)
                    }
                }
                waitImages()
            }
            override fun onReceivedError(view: WebView, request: WebResourceRequest, error: WebResourceError) {
                if (request.isForMainFrame) {
                    Log.e(TAG, "MainFrame error: ${error.description}")
                    callback(null, Exception(error.description?.toString() ?: "WebView mainframe error"))
                } else {
                    Log.w(TAG, "Subresource error: ${error.description}")
                }
            }
            override fun onReceivedHttpError(view: WebView, request: WebResourceRequest, errorResponse: WebResourceResponse) {
                if (request.isForMainFrame) {
                    Log.e(TAG, "MainFrame HTTP ${errorResponse.statusCode}")
                    callback(null, Exception("HTTP ${errorResponse.statusCode}"))
                } else {
                    Log.w(TAG, "Subresource HTTP ${errorResponse.statusCode}")
                }
            }
        }

        // Usa tu dominio de base para que /static/... resuelva bien
        wv.loadDataWithBaseURL(
            "https://intracoe.incoe.cloud/",
            // Asegura viewport y sin márgenes
            """
        <!doctype html><html><head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>html,body{margin:0;padding:0;width:100%}</style>
        </head><body>
        $html
        </body></html>
        """.trimIndent(),
            "text/html", "UTF-8", null
        )
    }


    fun printTextTest(ctx: Context, mac: String, text: String = "TEST ESC/POS\nHola Mundo\n") {
        Thread {
            try {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S &&
                    ContextCompat.checkSelfPermission(ctx, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED
                ) return@Thread

                val dev = BluetoothAdapter.getDefaultAdapter()?.getRemoteDevice(mac) ?: return@Thread
                val sock = dev.createRfcommSocketToServiceRecord(SPP_UUID)
                BluetoothAdapter.getDefaultAdapter()?.cancelDiscovery()
                sock.connect()
                val os = sock.outputStream

                os.write(byteArrayOf(0x1B, 0x40))                 // ESC @ (init)
                os.write(byteArrayOf(0x1B, 0x61, 0x01))           // Centrado
                os.write(text.toByteArray(Charsets.UTF_8))        // Texto simple ASCII/UTF-8
                os.write(byteArrayOf(0x0A, 0x1B, 0x64, 0x03))     // LF + feed 3 líneas
                os.flush()
                os.close(); sock.close()
            } catch (_: Exception) { }
        }.start()
    }
    fun printUrlSilently(

        ctx: Context,
        url: String,
        mac: String,
        paperWidthPx: Int = 576
    ) {

        renderUrlToBitmap(ctx, url, paperWidthPx) { bmp, err ->
            if (bmp == null) return@renderUrlToBitmap
            Thread { runCatching { sendBitmapEscPosOverBt(ctx, mac, bmp) } }.start()
        }
    }

    private fun hasBtConnectPermission(ctx: Context): Boolean =
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S)
            ContextCompat.checkSelfPermission(ctx, Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED
        else true

    private fun getDevice(mac: String): BluetoothDevice? =
        BluetoothAdapter.getDefaultAdapter()?.getRemoteDevice(mac)


    private fun buildEscPosFromBitmap(ctx: Context, src: Bitmap): ByteArray {
        val w = src.width
        val h = src.height
        val bytesPerColumn = (w + 7) / 8      // columnas de 8px en X
        val bytesPerLine = bytesPerColumn * 3 // 24-dot → 3 bytes por columna
        val out = ByteArrayOutputStream()
        fun write(vararg b: Int) { b.forEach(out::write) }

        write(0x1B, 0x40)          // ESC @ init
        write(0x1B, 0x33, 24)      // ESC 3 n  -> interlineado 24

        val threshold = 160
        var y = 0
        var totalLines = 0
        Log.d(TAG, "Raster ESC*33 w=$w h=$h bytesPerColumn=$bytesPerColumn bytesPerLine=$bytesPerLine (24-dot)")

        while (y < h) {
            // ESC * m nL nH    -> m=33 (24-dot double density), n = BYTES DE LA LÍNEA
            write(0x1B, 0x2A, 33, bytesPerLine and 0xFF, (bytesPerLine shr 8) and 0xFF)

            var xByte = 0
            while (xByte < bytesPerColumn) {
                var b0 = 0; var b1 = 0; var b2 = 0
                for (bit in 0 until 8) {
                    val x = xByte * 8 + bit
                    if (x < w) {
                        // banda 0
                        val yy0 = y + bit
                        if (yy0 < h) {
                            val c = src.getPixel(x, yy0)
                            val r = (c shr 16) and 0xFF
                            val g = (c shr 8) and 0xFF
                            val b = c and 0xFF
                            if ((r + g + b) / 3 < threshold) b0 = b0 or (1 shl (7 - bit))
                        }
                        // banda 1
                        val yy1 = y + 8 + bit
                        if (yy1 < h) {
                            val c = src.getPixel(x, yy1)
                            val r = (c shr 16) and 0xFF
                            val g = (c shr 8) and 0xFF
                            val b = c and 0xFF
                            if ((r + g + b) / 3 < threshold) b1 = b1 or (1 shl (7 - bit))
                        }
                        // banda 2
                        val yy2 = y + 16 + bit
                        if (yy2 < h) {
                            val c = src.getPixel(x, yy2)
                            val r = (c shr 16) and 0xFF
                            val g = (c shr 8) and 0xFF
                            val b = c and 0xFF
                            if ((r + g + b) / 3 < threshold) b2 = b2 or (1 shl (7 - bit))
                        }
                    }
                }
                out.write(b0); out.write(b1); out.write(b2)
                xByte++
            }
            out.write(0x0A) // LF para imprimir la banda de 24 puntos
            y += 24
            totalLines++
        }

        val bytes = out.toByteArray()
        Log.d(TAG, "ESC*33: w=$w h=$h bytes/col=$bytesPerColumn bytes/linea=$bytesPerLine lineas=$totalLines total=${bytes.size}")
        // Guarda una copia para inspección
        try {
            val f = File(ctx.cacheDir, "last_escpos.bin")
            FileOutputStream(f).use { it.write(bytes) }
            Log.d(TAG, "ESC/POS guardado en: ${f.absolutePath}")
        } catch (e: Exception) { Log.w(TAG, "No se pudo guardar ESC/POS", e) }

        return bytes
    }

    private fun renderUrlToBitmap(
        ctx: Context,
        url: String,
        widthPx: Int,
        callback: (Bitmap?, Throwable?) -> Unit
    ) {
        Log.d(TAG, "renderUrlToBitmap: url=$url widthPx=$widthPx")
        val wv = WebView(ctx)
        with(wv.settings) {
            javaScriptEnabled = true
            domStorageEnabled = true
            useWideViewPort = true
            loadWithOverviewMode = true
            mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
            blockNetworkImage = false
        }
        CookieManager.getInstance().setAcceptCookie(true)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            CookieManager.getInstance().setAcceptThirdPartyCookies(wv, true)
        }
        wv.layoutParams = ViewGroup.LayoutParams(widthPx, ViewGroup.LayoutParams.WRAP_CONTENT)

        fun drawWithHeightPx(view: WebView, heightPx: Int) {
            val h = heightPx.coerceAtLeast(1)
            val wSpec = View.MeasureSpec.makeMeasureSpec(widthPx, View.MeasureSpec.EXACTLY)
            val hSpec = View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED)
            view.measure(wSpec, hSpec)
            view.layout(0, 0, widthPx, h)
            val bmp = Bitmap.createBitmap(widthPx, h, Bitmap.Config.ARGB_8888)
            Canvas(bmp).apply { view.draw(this) }
            try {
                val f = File(ctx.cacheDir, "last_bitmap_url.png")
                FileOutputStream(f).use { bmp.compress(Bitmap.CompressFormat.PNG, 100, it) }
                Log.d(TAG, "Bitmap URL guardado: ${f.absolutePath} (${bmp.width}x${bmp.height})")
            } catch (_: Exception) { }
            callback(bmp, null)
        }

        fun measureAndDraw(view: WebView, attempt: Int = 0) {
            view.evaluateJavascript(
                "(function(){var d=document;var h=Math.max(d.body?d.body.scrollHeight:0,d.documentElement?d.documentElement.scrollHeight:0);return h;})()"
            ) { cssHStr ->
                val cssH = cssHStr?.replace("\"", "")?.toFloatOrNull() ?: 0f
                val pxByScale = (cssH * view.scale).toInt()
                val pxByDp = (cssH * ctx.resources.displayMetrics.density).toInt()
                val ch = (view.contentHeight * view.scale).toInt()
                val best = listOf(pxByScale, pxByDp, ch).maxOrNull() ?: 0

                Log.d(TAG, "measure(URL): cssH=$cssH scale=${view.scale} → pxByScale=$pxByScale pxByDp=$pxByDp contentPx=$ch best=$best attempt=$attempt")

                if (best > 1) {
                    drawWithHeightPx(view, best)
                } else if (attempt < 10) {
                    view.postDelayed({ measureAndDraw(view, attempt + 1) }, 150)
                } else {
                    callback(null, Exception("Nada que renderizar (height=0)"))
                }
            }
        }

        wv.webChromeClient = object : WebChromeClient() {
            override fun onConsoleMessage(cm: android.webkit.ConsoleMessage): Boolean {
                Log.d(TAG, "console[${cm.messageLevel()}] ${cm.sourceId()}:${cm.lineNumber()} ${cm.message()}")
                return false
            }
        }
        wv.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView, finishedUrl: String?) {
                Log.d(TAG, "URL onPageFinished; contentHeight=${view.contentHeight} scale=${view.scale}")
                // Espera a que las imágenes acaben
                fun waitImages(attempt: Int = 0) {
                    view.evaluateJavascript(
                        "(function(){try{var a=[].slice.call(document.images);return a.length===0||a.every(i=>i.complete);}catch(e){return true}})();"
                    ) { all ->
                        val ok = all == "true"
                        if (ok) measureAndDraw(view)
                        else if (attempt < 10) view.postDelayed({ waitImages(attempt + 1) }, 120)
                        else measureAndDraw(view)
                    }
                }
                waitImages()
            }
            override fun onReceivedError(view: WebView, request: WebResourceRequest, error: WebResourceError) {
                if (request.isForMainFrame) {
                    Log.e(TAG, "MainFrame error: ${error.description}")
                    callback(null, Exception(error.description?.toString() ?: "WebView mainframe error"))
                } else {
                    Log.w(TAG, "Subresource error: ${error.description}")   // ← ORB/404 de favicon o imágenes externas: no rompe
                }
            }
            override fun onReceivedHttpError(view: WebView, request: WebResourceRequest, errorResponse: WebResourceResponse) {
                if (request.isForMainFrame) {
                    Log.e(TAG, "MainFrame HTTP ${errorResponse.statusCode}")
                    callback(null, Exception("HTTP ${errorResponse.statusCode}"))
                } else {
                    Log.w(TAG, "Subresource HTTP ${errorResponse.statusCode}") // ← 404 de /favicon.ico es normal
                }
            }
        }

        runCatching { CookieManager.getInstance().getCookie(url) }
            .onSuccess { Log.d(TAG, "Cookies para $url: ${it?.take(120)}") }

        wv.loadUrl(url)
    }

    @SuppressLint("MissingPermission")
    private fun sendBitmapEscPosOverBt(ctx: Context, mac: String, src: Bitmap) {
        if (!hasBtConnectPermission(ctx)) { Log.w(TAG, "Sin permiso BLUETOOTH_CONNECT"); return }
        Log.d(TAG, "sendBitmapEscPosOverBt: bmp=${src.width}x${src.height} mac=$mac")

        val dev = getDevice(mac) ?: run { Log.e(TAG, "Device NULL"); return }
        try {
            val sock = dev.createRfcommSocketToServiceRecord(SPP_UUID)
            BluetoothAdapter.getDefaultAdapter()?.cancelDiscovery()
            Log.d(TAG, "Conectando socket...")
            sock.connect()
            Log.d(TAG, "Conectado ✓")
            val os = sock.outputStream

            // ✅ SOLO una versión: la nueva firma con ctx + src
            val data = buildEscPosFromBitmap(ctx, src)
            Log.d(TAG, "Bytes ESC/POS a enviar: ${data.size}")
            os.write(data); os.flush()

            // Feed 3 líneas (RPP300 no corta papel)
            os.write(byteArrayOf(0x1B, 0x64, 0x03)); os.flush()
            os.close(); sock.close()
            Log.d(TAG, "Envío terminado ✓")
        } catch (e: Exception) {
            Log.e(TAG, "Error enviando a impresora", e)
        }
    }



}