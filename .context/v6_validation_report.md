# iContext v6: validación técnica final

Implementación, distribución y sincronización completadas en los cinco repositorios. Las seis skills v6 están instaladas en Antigravity y Codex; los respaldos anteriores permanecen conservados.

Pruebas automatizadas: **238 aprobadas**. Contratos JSON persistidos: **30 válidos**. Instalación repetida: **0 escrituras**.

| Proyecto | Pruebas | Consulta p95 (ms) | Proceso p95 (ms) | Reducción auditoría incremental |
| :--- | ---: | ---: | ---: | ---: |
| iDirectory | 77 | 11.99 | 357.79 | 91.3% |
| ThinkingSeed | 6 | 8.11 | 306.29 | 88.0% |
| MetricsThinking | 116 | 10.59 | 336.23 | 91.3% |
| iReadme | 15 | 8.83 | 387.70 | 85.1% |
| ContextControl | 24 | 7.31 | 370.50 | 86.5% |

En las siete muestras calientes de cada proyecto se registraron **0 archivos releídos y 0 análisis AST repetidos**. Los paquetes Tier 1A consumen entre 142 y 154 tokens estimados; los de ecosistema, entre 228 y 244.

Comprobaciones finales: `audit --full`, `doctor`, auditoría de gobernanza y `reconcile --check` válidos en los cinco repositorios. Consultas, auditorías y `sync --dry-run` no cambiaron archivos ni timestamps; la segunda sincronización tampoco produjo cambios. Solicitudes de actualización pendientes: **0**.

Se probaron los cinco runtimes sin repositorios hermanos y los doce launchers globales. El checkpoint y el seed híbrido continuaron entre las instalaciones de Antigravity y Codex. Los manifiestos de runtime y todos los recursos de las skills coinciden con sus fuentes canónicas.

Uso: `icontext status`, `icontext pack <ruta>`, `icontext sync`, `icontext sync --all`, `icontext audit`, `icontext doctor`. Antigravity: `/idir`, `/seed`, `/seed-master`, `/metrics`, `/readme`, `/icontext`. Codex usa los mismos nombres con `$`. Si una sesión abierta conserva el catálogo anterior, recargar las skills o abrir una sesión nueva.

Alcance: tiempos locales sin inferencia del modelo; tokens estimados, no facturados. La comparación v5 usa su kernel 5.0 guardado en Git sobre los mismos proyectos actuales. Estas pruebas verifican motores y launchers; no miden decisiones, desvíos de alcance o tasa de éxito de sesiones LLM independientes. FPAI es auxiliar y la búsqueda de PII no certifica seguridad completa.

Los datos completos, muestras y huellas están en `v6_validation.json`; cada repositorio conserva su `benchmark_v6.json`, estados de capa y evidencias de comprobación.
