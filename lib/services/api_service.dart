import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static String baseUrl = 'http://192.168.140.10:5000';

  // Cargar IP guardada al iniciar
  static Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final savedIp = prefs.getString('server_ip');
    if (savedIp != null && savedIp.isNotEmpty) {
      baseUrl = 'http://$savedIp:5000';
    }
  }

  // Guardar nueva IP
  static Future<void> updateIp(String newIp) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('server_ip', newIp);
    baseUrl = 'http://$newIp:5000';
  }

  Future<Map<String, dynamic>> marcarAsistencia(String dni) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/api/marcar'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'dni': dni}),
          )
          .timeout(const Duration(seconds: 10));
      return jsonDecode(response.body);
    } catch (e) {
      return {'error': 'Error de conexión: $e'};
    }
  }

  Future<Map<String, dynamic>> login(String correo, String password) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/api/login'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'correo': correo.trim(),
              'password': password.trim(),
            }),
          )
          .timeout(const Duration(seconds: 7));
      return jsonDecode(response.body);
    } catch (e) {
      print("DEBUG LOGIN ERROR: $e");
      return {'status': 'error', 'mensaje': 'Error técnico: $e'};
    }
  }

  Future<List<dynamic>> getStats() async {
    final response = await http.get(Uri.parse('$baseUrl/api/asistencias/hoy'));
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return [10, data.length];
    }
    return [0, 0];
  }

  // --- NUEVOS MÉTODOS ---

  String getQRUrl(String dni) => '$baseUrl/api/empleado/$dni/qr';

  Future<Map<String, dynamic>> getEmpleadoDatos(String dni) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/empleado/$dni/datos'),
    );
    return jsonDecode(response.body);
  }

  Future<List<dynamic>> getListaEmpleados() async {
    final response = await http.get(Uri.parse('$baseUrl/api/admin/empleados'));
    if (response.statusCode == 200) return jsonDecode(response.body);
    return [];
  }

  Future<List<dynamic>> getListaHorarios() async {
    final response = await http.get(Uri.parse('$baseUrl/api/admin/horarios'));
    if (response.statusCode == 200) return jsonDecode(response.body);
    return [];
  }

  Future<Map<String, dynamic>> crearEmpleado(Map<String, dynamic> datos) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/admin/empleado/crear'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(datos),
    );
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> editarEmpleado(
    int id,
    Map<String, dynamic> datos,
  ) async {
    final response = await http.put(
      Uri.parse('$baseUrl/api/admin/empleado/editar/$id'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(datos),
    );
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> crearHorario(Map<String, dynamic> datos) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/admin/horario/crear'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(datos),
    );
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> editarHorario(
    int id,
    Map<String, dynamic> datos,
  ) async {
    final response = await http.put(
      Uri.parse('$baseUrl/api/admin/horario/editar/$id'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(datos),
    );
    return jsonDecode(response.body);
  }

  Future<List<dynamic>> getReporteGeneral() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/admin/reporte/general'),
    );
    if (response.statusCode == 200) return jsonDecode(response.body);
    return [];
  }

  Future<List<dynamic>> getReporteTardanzas() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/admin/reporte/tardanzas'),
    );
    if (response.statusCode == 200) return jsonDecode(response.body);
    return [];
  }
}
