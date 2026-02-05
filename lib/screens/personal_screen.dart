import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import '../services/api_service.dart';

class PersonalScreen extends StatefulWidget {
  final String? dniInicial;
  const PersonalScreen({super.key, this.dniInicial});

  @override
  State<PersonalScreen> createState() => _PersonalScreenState();
}

class _PersonalScreenState extends State<PersonalScreen> {
  late final TextEditingController _dniController;
  final _apiService = ApiService();
  Map<String, dynamic>? _datos;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _dniController = TextEditingController(text: widget.dniInicial);
    if (widget.dniInicial != null) {
      // Delay un poco para que la UI cargue
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _consultar();
      });
    }
  }

  void _consultar() async {
    if (_dniController.text.isEmpty) return;
    setState(() => _isLoading = true);
    try {
      final res = await _apiService.getEmpleadoDatos(_dniController.text);
      setState(() => _datos = res);
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Error al consultar datos")));
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("MI ASISTENCIA")),
      body: Container(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            if (widget.dniInicial == null)
              FadeInDown(
                child: Card(
                  color: const Color(0xFF1E293B),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _dniController,
                            decoration: const InputDecoration(
                              labelText: "Ingresa tu DNI",
                              prefixIcon: Icon(
                                Icons.badge,
                                color: Color(0xFFD4AF37),
                              ),
                            ),
                            keyboardType: TextInputType.number,
                          ),
                        ),
                        const SizedBox(width: 10),
                        IconButton(
                          onPressed: _consultar,
                          icon: const Icon(
                            Icons.search,
                            color: Color(0xFFD4AF37),
                          ),
                          style: IconButton.styleFrom(
                            backgroundColor: Colors.white10,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            const SizedBox(height: 20),
            if (_isLoading)
              const CircularProgressIndicator(color: Color(0xFFD4AF37))
            else if (_datos != null && _datos!['error'] == null)
              Expanded(
                child: Column(
                  children: [
                    _buildQRSection(_datos!['dni']),
                    const SizedBox(height: 10),
                    Text(
                      _datos!['nombre'],
                      style: const TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFD4AF37),
                      ),
                    ),
                    const SizedBox(height: 5),
                    if (_datos!['horario'] != null)
                      FadeInUp(
                        child: Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 12,
                            vertical: 6,
                          ),
                          decoration: BoxDecoration(
                            color: const Color(0xFFD4AF37).withOpacity(0.1),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(
                              color: const Color(0xFFD4AF37).withOpacity(0.3),
                            ),
                          ),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const Icon(
                                    Icons.access_time,
                                    size: 16,
                                    color: Color(0xFFD4AF37),
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    "${_datos!['horario']['turno']}: ${_datos!['horario']['inicio']} - ${_datos!['horario']['fin']}",
                                    style: const TextStyle(
                                      color: Color(0xFFD4AF37),
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 4),
                              Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const Icon(
                                    Icons.calendar_month,
                                    size: 14,
                                    color: Color(0xFFD4AF37),
                                  ),
                                  const SizedBox(width: 6),
                                  Text(
                                    "${_datos!['horario']['dias']}",
                                    style: TextStyle(
                                      color: const Color(
                                        0xFFD4AF37,
                                      ).withOpacity(0.8),
                                      fontSize: 12,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ),
                    const SizedBox(height: 15),
                    Expanded(
                      child: DefaultTabController(
                        length: 2,
                        child: Column(
                          children: [
                            const TabBar(
                              tabs: [
                                Tab(
                                  text: "Asistencias",
                                  icon: Icon(Icons.history),
                                ),
                                Tab(
                                  text: "Permisos",
                                  icon: Icon(Icons.assignment_turned_in),
                                ),
                              ],
                              indicatorColor: Color(0xFFD4AF37),
                              labelColor: Color(0xFFD4AF37),
                            ),
                            Expanded(
                              child: TabBarView(
                                children: [
                                  _buildAsistenciasList(_datos!['asistencias']),
                                  _buildPermisosList(_datos!['permisos']),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              )
            else if (_datos != null)
              const Text("No se encontraron datos para este DNI"),
          ],
        ),
      ),
    );
  }

  Widget _buildQRSection(String dni) {
    final qrUrl = _apiService.getQRUrl(dni);
    return FadeInDown(
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFFD4AF37).withOpacity(0.2),
              blurRadius: 15,
            ),
          ],
        ),
        child: Image.network(
          qrUrl,
          width: 140,
          height: 140,
          errorBuilder: (context, error, stackTrace) {
            return const Icon(Icons.broken_image, size: 50, color: Colors.grey);
          },
          loadingBuilder: (context, child, loadingProgress) {
            if (loadingProgress == null) return child;
            return const SizedBox(
              width: 140,
              height: 140,
              child: Center(child: CircularProgressIndicator()),
            );
          },
        ),
      ),
    );
  }

  Widget _buildAsistenciasList(List<dynamic> lista) {
    if (lista.isEmpty) return const Center(child: Text("Sin registros"));
    return ListView.builder(
      padding: const EdgeInsets.symmetric(vertical: 10),
      itemCount: lista.length,
      itemBuilder: (context, index) {
        final item = lista[index];
        // Determinar si fue tarde (Asumimos que el backend podría enviar un flag, pero si no, podemos inferirlo o confiar en que el backend ya lo calculó en la ruta de reporte)
        // Por ahora, vamos a darle un estilo elegante
        return FadeInLeft(
          delay: Duration(milliseconds: index * 50),
          child: Container(
            margin: const EdgeInsets.only(bottom: 12),
            decoration: BoxDecoration(
              color: const Color(0xFF1E293B),
              borderRadius: BorderRadius.circular(15),
              border: Border.all(color: Colors.white10),
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 20,
                vertical: 8,
              ),
              leading: Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: const Color(0xFFD4AF37).withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.calendar_today,
                  color: Color(0xFFD4AF37),
                  size: 20,
                ),
              ),
              title: Text(
                item['fecha'],
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                ),
              ),
              subtitle: Padding(
                padding: const EdgeInsets.only(top: 5),
                child: Row(
                  children: [
                    const Icon(
                      Icons.login,
                      size: 14,
                      color: Colors.greenAccent,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      item['entrada'],
                      style: const TextStyle(color: Colors.white70),
                    ),
                    const SizedBox(width: 15),
                    const Icon(Icons.logout, size: 14, color: Colors.redAccent),
                    const SizedBox(width: 4),
                    Text(
                      item['salida'],
                      style: const TextStyle(color: Colors.white70),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildPermisosList(List<dynamic> lista) {
    if (lista.isEmpty)
      return const Center(child: Text("Sin permisos registrados"));
    return ListView.builder(
      itemCount: lista.length,
      itemBuilder: (context, index) {
        final item = lista[index];
        return Card(
          margin: const EdgeInsets.symmetric(vertical: 5),
          child: ListTile(
            leading: const Icon(Icons.verified, color: Colors.green),
            title: Text(item['tipo']),
            subtitle: Text("${item['fecha']}\n${item['descripcion']}"),
          ),
        );
      },
    );
  }
}
