import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import 'services/api_service.dart';
import 'screens/horarios_screen.dart';
import 'screens/personal_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _correoController = TextEditingController();
  final _passController = TextEditingController();
  final _apiService = ApiService();
  bool _isLoading = false;

  void _login() async {
    if (_correoController.text.isEmpty || _passController.text.isEmpty) {
      _showError("Por favor, complete todos los campos");
      return;
    }

    setState(() => _isLoading = true);
    try {
      final res = await _apiService.login(
        _correoController.text,
        _passController.text,
      );
      if (mounted) {
        if (res['status'] == 'success') {
          if (res['rol'] == 'admin') {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => const DashboardScreen()),
            );
          } else {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (context) => PersonalScreen(dniInicial: res['dni']),
              ),
            );
          }
        } else {
          // Si hubo un error técnico o credenciales inválidas, mostrar el mensaje exacto
          _showError(res['mensaje'] ?? "Credenciales incorrectas");
        }
      }
    } catch (e) {
      if (mounted) _showError("Error inesperado: $e");
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  void _showError(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
        backgroundColor: Colors.redAccent,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ACCESO AL SISTEMA'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings_ethernet, color: Color(0xFFD4AF37)),
            onPressed: _showIPConfig,
            tooltip: 'Configurar IP del Servidor',
          ),
        ],
      ),
      body: Container(
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0F172A), Color(0xFF1E293B)],
          ),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(30.0),
          child: Column(
            children: [
              const SizedBox(height: 20),
              FadeInDown(
                child: const Icon(
                  Icons.lock_person,
                  size: 80,
                  color: Color(0xFFD4AF37),
                ),
              ),
              const SizedBox(height: 40),
              FadeInRight(
                child: TextField(
                  controller: _correoController,
                  decoration: const InputDecoration(
                    labelText: 'DNI o Correo Electrónico',
                    prefixIcon: Icon(Icons.person, color: Color(0xFFD4AF37)),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              FadeInLeft(
                child: TextField(
                  controller: _passController,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Contraseña',
                    prefixIcon: Icon(Icons.key, color: Color(0xFFD4AF37)),
                  ),
                ),
              ),
              const SizedBox(height: 40),
              FadeInUp(
                child: _isLoading
                    ? const CircularProgressIndicator(color: Color(0xFFD4AF37))
                    : ZoomIn(
                        child: ElevatedButton(
                          onPressed: _login,
                          style: ElevatedButton.styleFrom(
                            minimumSize: const Size(double.infinity, 55),
                            elevation: 8,
                          ),
                          child: const Text(
                            'INICIAR SESIÓN',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
              ),
              const SizedBox(height: 30),
              Text(
                "Servidor: ${ApiService.baseUrl.replaceAll('http://', '').replaceAll(':5000', '')}",
                style: const TextStyle(color: Colors.white24, fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showIPConfig() {
    final ipController = TextEditingController(
      text: ApiService.baseUrl
          .replaceAll('http://', '')
          .replaceAll(':5000', ''),
    );
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text('Configurar IP del Servidor'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Ingresa la IP de tu PC para conectar la app:',
              style: TextStyle(fontSize: 14, color: Colors.white70),
            ),
            const SizedBox(height: 15),
            TextField(
              controller: ipController,
              decoration: const InputDecoration(
                hintText: 'Ej: 192.168.1.15',
                labelText: 'Dirección IP',
              ),
              keyboardType: TextInputType.number,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('CANCELAR'),
          ),
          ElevatedButton(
            onPressed: () async {
              if (ipController.text.isNotEmpty) {
                await ApiService.updateIp(ipController.text.trim());
                if (mounted) {
                  Navigator.pop(context);
                  setState(() {}); // Refrescar para mostrar la nueva IP
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('IP actualizada correctamente'),
                    ),
                  );
                }
              }
            },
            child: const Text('GUARDAR'),
          ),
        ],
      ),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PANEL DE CONTROL'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (context) => const LoginScreen()),
                (route) => false,
              );
            },
          ),
        ],
      ),
      body: FadeInUp(
        child: GridView.count(
          padding: const EdgeInsets.all(20),
          crossAxisCount: 2,
          mainAxisSpacing: 20,
          crossAxisSpacing: 20,
          children: [
            _buildCard(context, 'Personal', Icons.people, Colors.blue, () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const PersonnelManagementScreen(),
                ),
              );
            }),
            _buildCard(context, 'Horarios', Icons.schedule, Colors.green, () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const HorariosManagementScreen(),
                ),
              );
            }),
            _buildCard(
              context,
              'Reporte Diario',
              Icons.assessment,
              Colors.orange,
              () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const GeneralReportScreen(),
                  ),
                );
              },
            ),
            _buildCard(context, 'Tardanzas', Icons.alarm, Colors.red, () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const TardanzasReportScreen(),
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildCard(
    BuildContext context,
    String title,
    IconData icon,
    Color color,
    VoidCallback onTap,
  ) {
    return Card(
      elevation: 8,
      color: const Color(0xFF1E293B),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
        side: BorderSide(color: color.withOpacity(0.3)),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, size: 40, color: color),
            ),
            const SizedBox(height: 12),
            Text(
              title,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class PersonnelManagementScreen extends StatefulWidget {
  const PersonnelManagementScreen({super.key});

  @override
  State<PersonnelManagementScreen> createState() =>
      _PersonnelManagementScreenState();
}

class _PersonnelManagementScreenState extends State<PersonnelManagementScreen> {
  final _apiService = ApiService();
  List<dynamic> _empleados = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadEmpleados();
  }

  void _loadEmpleados() async {
    setState(() => _isLoading = true);
    final list = await _apiService.getListaEmpleados();
    setState(() {
      _empleados = list;
      _isLoading = false;
    });
  }

  void _abrirFormulario({Map<String, dynamic>? empleado}) async {
    final dniController = TextEditingController(text: empleado?['dni']);
    final nombreController = TextEditingController(text: empleado?['nombre']);
    final apellidoController = TextEditingController(
      text: empleado?['apellido'],
    );
    int? selectedHorario = empleado?['idHorario'];
    List<dynamic> horarios = await _apiService.getListaHorarios();

    if (!mounted) return;

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          backgroundColor: const Color(0xFF1E293B),
          title: Text(empleado == null ? "Nuevo Empleado" : "Editar Empleado"),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: dniController,
                  decoration: const InputDecoration(labelText: "DNI"),
                ),
                TextField(
                  controller: nombreController,
                  decoration: const InputDecoration(labelText: "Nombre"),
                ),
                TextField(
                  controller: apellidoController,
                  decoration: const InputDecoration(labelText: "Apellido"),
                ),
                const SizedBox(height: 10),
                DropdownButtonFormField<int>(
                  value: selectedHorario,
                  items: horarios
                      .map(
                        (h) => DropdownMenuItem<int>(
                          value: h['id'],
                          child: Text(h['turno']),
                        ),
                      )
                      .toList(),
                  onChanged: (val) =>
                      setDialogState(() => selectedHorario = val),
                  decoration: const InputDecoration(labelText: "Horario"),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("CANCELAR"),
            ),
            ElevatedButton(
              onPressed: () async {
                final datos = {
                  'dni': dniController.text,
                  'nombre': nombreController.text,
                  'apellido': apellidoController.text,
                  'idHorario': selectedHorario,
                };
                if (empleado == null) {
                  await _apiService.crearEmpleado(datos);
                } else {
                  await _apiService.editarEmpleado(empleado['id'], datos);
                }
                if (mounted) {
                  Navigator.pop(context);
                  _loadEmpleados();
                }
              },
              child: const Text("GUARDAR"),
            ),
          ],
        ),
      ),
    );
  }

  void _showQR(String dni, String nombre) {
    showDialog(
      context: context,
      builder: (context) => ZoomIn(
        child: AlertDialog(
          backgroundColor: const Color(0xFF1E293B),
          title: Text(nombre, textAlign: TextAlign.center),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Image.network(
                  _apiService.getQRUrl(dni),
                  width: 200,
                  height: 200,
                  errorBuilder: (context, error, stackTrace) =>
                      const Icon(Icons.error, size: 50, color: Colors.red),
                ),
              ),
              const SizedBox(height: 10),
              const Text(
                "DNI: ",
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              Text(dni),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("CERRAR"),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("GESTIÓN DE PERSONAL")),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _abrirFormulario(),
        child: const Icon(Icons.add),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(10),
              itemCount: _empleados.length,
              itemBuilder: (context, index) {
                final emp = _empleados[index];
                return FadeInLeft(
                  delay: Duration(milliseconds: index * 100),
                  child: Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: emp['estado'] == 'Activo'
                            ? Colors.green
                            : Colors.grey,
                        child: const Icon(Icons.person, color: Colors.white),
                      ),
                      title: Text("${emp['nombre']} ${emp['apellido']}"),
                      subtitle: Text("DNI: ${emp['dni']} | ${emp['horario']}"),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          IconButton(
                            icon: const Icon(
                              Icons.qr_code,
                              color: Color(0xFFD4AF37),
                            ),
                            onPressed: () => _showQR(emp['dni'], emp['nombre']),
                          ),
                          IconButton(
                            icon: const Icon(Icons.edit, color: Colors.blue),
                            onPressed: () => _abrirFormulario(empleado: emp),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
    );
  }
}

class GeneralReportScreen extends StatefulWidget {
  const GeneralReportScreen({super.key});

  @override
  State<GeneralReportScreen> createState() => _GeneralReportScreenState();
}

class _GeneralReportScreenState extends State<GeneralReportScreen> {
  final _apiService = ApiService();
  List<dynamic> _data = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadReport();
  }

  void _loadReport() async {
    setState(() => _isLoading = true);
    final list = await _apiService.getReporteGeneral();
    setState(() {
      _data = list;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("REPORTE GENERAL")),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(10),
              itemCount: _data.length,
              itemBuilder: (context, index) {
                final item = _data[index];
                bool isTarde = item['estado'] == 'Tarde';
                return FadeInUp(
                  delay: Duration(milliseconds: index * 50),
                  child: Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text("${item['nombre']} (${item['fecha']})"),
                      subtitle: Text(
                        "Entrada: ${item['entrada']} | Salida: ${item['salida']}\nTotal: ${item['horas']}",
                      ),
                      trailing: Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 10,
                          vertical: 5,
                        ),
                        decoration: BoxDecoration(
                          color: isTarde
                              ? Colors.red.withOpacity(0.2)
                              : Colors.green.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Text(
                          item['estado'],
                          style: TextStyle(
                            color: isTarde ? Colors.red : Colors.green,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
    );
  }
}

class TardanzasReportScreen extends StatefulWidget {
  const TardanzasReportScreen({super.key});

  @override
  State<TardanzasReportScreen> createState() => _TardanzasReportScreenState();
}

class _TardanzasReportScreenState extends State<TardanzasReportScreen> {
  final _apiService = ApiService();
  List<dynamic> _data = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadReport();
  }

  void _loadReport() async {
    setState(() => _isLoading = true);
    final list = await _apiService.getReporteTardanzas();
    setState(() {
      _data = list;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("REPORTE DE TARDANZAS")),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(10),
              itemCount: _data.length,
              itemBuilder: (context, index) {
                final item = _data[index];
                return FadeInUp(
                  delay: Duration(milliseconds: index * 50),
                  child: Card(
                    color: Colors.red.withOpacity(0.05),
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(
                        Icons.warning_amber_rounded,
                        color: Colors.red,
                      ),
                      title: Text("${item['nombre']} (${item['fecha']})"),
                      subtitle: Text(
                        "Entrada: ${item['entrada']}\nRetraso: ${item['retraso']}",
                      ),
                    ),
                  ),
                );
              },
            ),
    );
  }
}
