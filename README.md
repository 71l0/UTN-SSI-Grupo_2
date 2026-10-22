# UTN-SSI-Grupo_2

[![Pipeline DevSecOps](https://github.com/71l0/UTN-SSI-Grupo_2/actions/workflows/devsecops.yml/badge.svg?branch=main&event=push)](https://github.com/71l0/UTN-SSI-Grupo_2/actions/workflows/devsecops.yml)

# Demo DevSecOps: pipeline que bloquea una app vulnerable

Caso práctico para la monografía. Una misma aplicación web (Flask) existe en dos versiones:

| Carpeta | Contenido |
|---|---|
| `vulnerable/` | 4 fallas intencionales: secreto en el código, inyección SQL, `debug=True` y dependencias con CVE conocidas |
| `secure/` | Las 4 corregidas: secreto desde el entorno, consulta parametrizada, debug apagado, dependencias actualizadas y cabeceras de seguridad |

Un pipeline CI/CD ejecuta controles automáticos y **bloquea** la versión vulnerable.

## El pipeline

| Etapa | Herramienta | Qué detecta | Riesgo que cubre |
|---|---|---|---|
| 1. Secretos | Gitleaks | Clave de API escrita en el código | CICD-SEC-6 (Cider) |
| 2. SAST | Semgrep (`semgrep-rules.yml`) | Inyección SQL y `debug=True` | PW.7 (NIST SSDF) |
| 3. SCA | pip-audit | 23 vulnerabilidades en Flask/Werkzeug 2.2.2 | CICD-SEC-3 (Cider), PW.4.4 (NIST) |
| 4. DAST | OWASP ZAP (solo informe) | Fallas del sitio en ejecución | PW.8 (NIST) |

Las etapas 1 a 3 frenan el pipeline si encuentran algo. La 4 genera un informe descargable y no bloquea.

## Resultados verificados en una prueba local

| | `vulnerable` | `secure` |
|---|---|---|
| Gitleaks | 1 secreto → falla | sin secretos → pasa |
| Semgrep | 2 hallazgos → falla | 0 hallazgos → pasa |
| pip-audit | 23 vulnerabilidades → falla | sin vulnerabilidades → pasa |
| Ataque `' OR '1'='1` en `/user` | devuelve **todos** los usuarios | devuelve lista vacía |

## Cómo ejecutarlo

**Local:**
```bash
pip install semgrep pip-audit      # y tener gitleaks en el PATH
./run_checks.sh vulnerable         # termina en ❌ PIPELINE BLOQUEADO
./run_checks.sh secure             # termina en ✅ PIPELINE APROBADO
```

**En GitHub (recomendado para presentar):**
1. Creá un repositorio nuevo y subí todo este contenido (incluida la carpeta `.github`).
2. Pestaña **Actions → DevSecOps Pipeline → Run workflow**.
3. Elegí `vulnerable` y ejecutá: los jobs 1, 2 y 3 se ponen en rojo y el DAST no llega a correr.
4. Volvé a ejecutar eligiendo `secure`: todo en verde y se publica el informe de ZAP.

## Guion de la presentación (5-7 min)

1. **Problema (1 min):** mostrar `vulnerable/app.py` y señalar las 4 fallas marcadas con `[Falla N]`.
2. **Demostrar el daño (1 min):** en `/user?name=' OR '1'='1` la versión vulnerable devuelve todos los usuarios.
3. **Pipeline en acción (2 min):** ejecutar con `vulnerable` y mostrar qué etapa detecta cada falla.
4. **Solución (1 min):** comparar `vulnerable/app.py` con `secure/app.py` (diff lado a lado).
5. **Pipeline en verde (1 min):** ejecutar con `secure`, abrir el informe de ZAP.
6. **Cierre:** conectar con *shift left*: el error se detecta en minutos y antes de llegar a producción.

## Límites a mencionar

- La clave de API es **falsa**, inventada para la demo.
- Es una aplicación pequeña: ilustra el flujo, no reemplaza un pipeline de producción.
- Las reglas de Semgrep son propias y mínimas; en un proyecto real se suman las reglas públicas (`p/python`).
- La etapa DAST no se probó en esta demo. Se ejecuta en GitHub Actions y puede requerir ajustes.
- Las etapas 1 a 3 sí se probaron localmente; el workflow de GitHub no se corrió.
