"""
Report Renderer for MetricsThinking™.
Generates rich Markdown audit reports with optimized horizontal Mermaid diagrams (LR),
JSON telemetry exports, and operational 10-phase INFERRED_ROADMAP.md.
"""

import json
import sys
from pathlib import Path

# Ensure local directory is in sys.path for standalone script execution
_PKG_DIR = Path(__file__).resolve().parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

try:
    from metricsthinking.models import ModuleStatus, ProjectAuditReport
except (ImportError, ValueError):
    try:
        from .models import ModuleStatus, ProjectAuditReport
    except (ImportError, ValueError):
        from models import ModuleStatus, ProjectAuditReport


class ReportRenderer:
    """Renders the ProjectAuditReport into Markdown, JSON, and INFERRED_ROADMAP formats."""

    def __init__(self, report: ProjectAuditReport):
        self.report = report

    def render_markdown(self) -> str:
        """Assembles the complete executive and forensic Markdown audit report."""
        sections = [
            self._render_header(),
            self._render_executive_summary(),
            self._render_dashboard_table(),
            self._render_mermaid_roadmap(),
            self._render_forensic_breakdown(),
            self._render_remediation_plan(),
            self._render_spectral_context_efficiency(),
            self._render_security_and_attack_surface(),
            self._render_systems_modularity_and_resilience(),
            self._render_footer()
        ]
        return "\n\n".join(sections)

    def render_inferred_roadmap(self) -> str:
        """Generates the decoupled operational roadmap in 10 phases with interactive checklists."""
        lines = [
            "---",
            'id: "inferred_roadmap"',
            f'title: "INFERRED OPERATIONAL ROADMAP: {self.report.project_name.upper()}"',
            'status: "active"',
            "executable: true",
            'version: "5.0"',
            "---",
            f"# INFERRED OPERATIONAL ROADMAP: {self.report.project_name.upper()}",
            "",
            f"> **Framework de Gobernanza:** MetricsThinking™ v5.0 Universal ({self.report.domain_archetype.value.upper()} / Stage-Gate)  ",
            f"> **Arquetipo de Dominio:** `{self.report.domain_archetype.value}` | **Modo:** `{self.report.inspection_mode.value}`  ",
            f"> **Estado Consolidado:** `{self.report.consolidated_score:.1f}% / 100.0%` — **{self.report.maturity_band.value}**  ",
            f"> **Cuello de Botella Activo:** `{self.report.active_bottleneck}`  ",
            f"> **Fecha de Emisión:** `{self.report.audit_date}`  ",
            "",
            "Este documento representa el **Roadmap Operacional y de Ejecución Técnica** derivado por ingeniería inversa a partir de la evidencia física (Ground Truth) del repositorio. Sirve como guía de trabajo para el equipo de arquitectura y desarrollo.",
            "",
            "---",
            ""
        ]

        for m in self.report.modules:
            status_badge = "🟢 COMPLETADO" if m.status == ModuleStatus.DONE else (
                "🔵 EN CONSTRUCCIÓN" if m.status == ModuleStatus.ACTIVE else "⚪ BACKLOG"
            )
            lines.append(f"## {m.module_id}: {m.name}")
            lines.append(f"**Avance:** `{m.phase_completion_pct:.1f}%` | **Peso en Ciclo:** `{m.weight * 100:.0f}%` | **Estado:** {status_badge}")
            lines.append("")
            lines.append("### Checklists de Implementación")

            for crit in m.criteria:
                if crit.fulfilled:
                    evidence_str = f" *(Evidencia: `{crit.evidence_path}`)*" if crit.evidence_path else ""
                    lines.append(f"- [x] **{crit.name}** (`{crit.criterion_id}`): {crit.evidence_detail}{evidence_str}")
                else:
                    action_str = crit.remediation_hint or "Implementación requerida según contrato de especificación."
                    lines.append(f"- [ ] **{crit.name}** (`{crit.criterion_id}`): {action_str}")

            lines.append("")
            lines.append("### Entregables Tangibles Esperados")
            if m.status == ModuleStatus.DONE:
                lines.append(f"- ✅ Todos los artefactos y contratos físicos de **{m.module_id}** han sido verificados satisfactoriamente en disco.")
            else:
                missing_crits = [c.name for c in m.criteria if not c.fulfilled]
                lines.append(f"- 🎯 Cierre de brechas pendientes: {', '.join(missing_crits)}.")
                lines.append("- 📁 Materialización de especificaciones formales, código nuclear, contratos de validación o pruebas automatizadas asociadas.")

            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append("> *Documento operacional generado automáticamente por **MetricsThinking™ Universal Project Auditor**.*")
        return "\n".join(lines)

    def write_artifacts(self, output_dir: Path | None = None, filename_prefix: str = "MetricsThinking") -> dict[str, Path]:
        """Writes Markdown, JSON, INFERRED_ROADMAP, and CONTEXT_PRUNING_PLAN artifacts to disk."""
        target_root = Path(self.report.project_path).resolve()

        # Canonical destination for all MetricsThinking artifacts (iDirectory / iContext Protocol v5.0)
        canonical_mt_dir = target_root / "artifacts" / "plans" / "metricsthinking"

        if output_dir is None:
            out_dir_path = canonical_mt_dir
        else:
            out_dir_path = Path(output_dir).resolve()
            # If pointing generically to root 'artifacts', redirect to canonical 'artifacts/plans/metricsthinking'
            if out_dir_path == target_root / "artifacts":
                out_dir_path = canonical_mt_dir

        out_dir_path.mkdir(parents=True, exist_ok=True)

        md_path = out_dir_path / f"{filename_prefix}.md"
        json_path = out_dir_path / f"{filename_prefix}.json"
        roadmap_path = out_dir_path / "INFERRED_ROADMAP.md"

        # Render content
        md_content = self.render_markdown()
        roadmap_content = self.render_inferred_roadmap()

        # Write Markdown & Roadmap
        md_path.write_text(md_content, encoding="utf-8")
        roadmap_path.write_text(roadmap_content, encoding="utf-8")

        # Write Context Pruning Plan if present
        pruning_path = None
        if self.report.pruning_plan:
            pruning_path = out_dir_path / "CONTEXT_PRUNING_PLAN.json"
            pruning_path.write_text(
                self.report.pruning_plan.model_dump_json(indent=2),
                encoding="utf-8"
            )

        # Write JSON
        json_data = self.report.model_dump()
        json_data["project_path"] = "./"
        json_data["consolidated_score"] = round(self.report.consolidated_score, 2)
        json_data["maturity_band"] = self.report.maturity_band.value
        json_data["active_bottleneck"] = self.report.active_bottleneck

        # Add computed module values to json
        for i, m in enumerate(self.report.modules):
            json_data["modules"][i]["phase_completion_pct"] = round(m.phase_completion_pct, 2)
            json_data["modules"][i]["weighted_contribution_pct"] = round(m.weighted_contribution_pct, 2)
            json_data["modules"][i]["status"] = m.status.value

        json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
        json_path.write_text(json_str, encoding="utf-8")

        from metricsthinking.runtime import publish_layer, read_json
        if out_dir_path == canonical_mt_dir:
            publish_layer(target_root, "l2", {"present": True, "state": "validated",
                "inputs_hash": read_json(target_root / ".context/inventory.json").get("inputs_hash"),
                "consolidated_score": round(self.report.consolidated_score, 2),
                "fpai_pf_spectral": self.report.fpai.power_factor_spectral if self.report.fpai else None,
                "fpai_s_spectral": self.report.fpai.s_spectral if self.report.fpai else None,
                "security_gate": (1.0 if self.report.security.pii_matches_count == 0 else 0.0) if self.report.security else None,
                "report_path": "artifacts/plans/metricsthinking/MetricsThinking.json"})

        artifacts_dict = {"markdown": md_path, "json": json_path, "roadmap": roadmap_path}
        if pruning_path:
            artifacts_dict["pruning"] = pruning_path
        return artifacts_dict

    def _render_header(self) -> str:
        score = self.report.consolidated_score
        band = self.report.maturity_band.value

        return f"""# METRICSTHINKING™: Auditoría Forense y Madurez del Proyecto

> **Motor Evaluador:** MetricsThinking™ v6.0 Universal  
> **Proyecto Auditado:** `{self.report.project_name}`  
> **Ubicación:** `./`  
> **Fecha de Auditoría:** `{self.report.audit_date}`  
> **Auditor Responsable:** `{self.report.auditor}`  
> **Perfil Aplicado:** `{self.report.profile_used}` (`{self.report.domain_archetype.value}`)  
> **Modo de Inspección:** `{self.report.inspection_mode.value}`  
> **ThinkingSeed:** {'`Detectado (v' + (self.report.seed_version or '3.0') + ')`' if self.report.seed_detected else '`No detectado`'}  
> **Git Commit / Branch:** `{self.report.git_commit or 'N/A'}` / `{self.report.git_branch or 'N/A'}`  
> **Score Consolidado:** **`{score:.1f}% / 100.0%`**  
> **Banda de Madurez:** **{band}**"""

    def _render_executive_summary(self) -> str:
        score = self.report.consolidated_score
        bottleneck = self.report.active_bottleneck

        total_criteria = sum(m.criteria_total for m in self.report.modules)
        passed_criteria = sum(m.criteria_passed for m in self.report.modules)

        primitives_table = ""
        if self.report.evidence_primitives:
            primitives_table = "\n\n### Primitivas Universales de Evidencia\n\n| Primitiva | Archivos Clasificados | Rutas de Muestra |\n|:---|:---:|:---|\n"
            for p_name, p_sum in self.report.evidence_primitives.items():
                samples = ", ".join(f"`{s}`" for s in p_sum.sample_paths[:3]) if p_sum.sample_paths else "—"
                primitives_table += f"| **{p_name.capitalize()}** | `{p_sum.file_count}` | {samples} |\n"

        return f"""---

## 1. RESUMEN EJECUTIVO Y GROUND TRUTH

MetricsThinking™ ha completado la auditoría forense estricta basada en evidencias físicas verificables en el repositorio.

- **Nota Global Consolidada ($Score_{{Total}}$):** **`{score:.2f}%`**
- **Arquetipo de Dominio:** **`{self.report.domain_archetype.value}`** (Modo: `{self.report.inspection_mode.value}`)
- **Criterios Cumplidos:** **`{passed_criteria} / {total_criteria}`** ({round((passed_criteria/total_criteria)*100, 1) if total_criteria else 0}%)
- **Cuello de Botella Inmediato:** **`{bottleneck}`**
- **Archivos Físicos Escaneados:** **`{self.report.stats.get('total_files_scanned', 0)}`**
- **Memoria Técnica (Seed):** {'`Presente`' if self.report.seed_detected or self.report.stats.get('seeds_detected', 0) > 0 else '`No detectada`'}
- **Gobernanza iDirectory (.context.yaml):** {'`Activa`' if self.report.stats.get('context_files_detected', 0) > 0 else '`No detectada`'}{primitives_table}"""

    def _render_dashboard_table(self) -> str:
        lines = [
            "---",
            "",
            "## 2. DASHBOARD EJECUTIVO DE MADUREZ POR MÓDULOS CANÓNICOS",
            "",
            "| ID | Nombre del Módulo | Peso ($W_i$) | Criterios Cumplidos | % Cumplimiento | Contribución ($S_i$) | Estado |",
            "|:---|:---|:---:|:---:|:---:|:---:|:---:|"
        ]

        for m in self.report.modules:
            status_icon = "🟢 Done" if m.status == ModuleStatus.DONE else (
                "🔵 Active" if m.status == ModuleStatus.ACTIVE else "⚪ Backlog"
            )
            lines.append(
                f"| **{m.module_id}** | {m.name} | **{m.weight * 100:.0f}%** | "
                f"`{m.criteria_passed} / {m.criteria_total}` | "
                f"**{m.phase_completion_pct:.1f}%** | "
                f"**{m.weighted_contribution_pct:.2f}%** | "
                f"{status_icon} |"
            )

        lines.append(
            f"| **TOTAL** | **Ciclo de Vida Completo ({self.report.domain_archetype.value.upper()})** | **100%** | "
            f"`{sum(m.criteria_passed for m in self.report.modules)} / {sum(m.criteria_total for m in self.report.modules)}` | "
            f"— | **`{self.report.consolidated_score:.2f}%`** | "
            f"**{self.report.maturity_band.name}** |"
        )

        return "\n".join(lines)

    def _render_mermaid_roadmap(self) -> str:
        """Renders the optimized, highly readable horizontal Mermaid roadmap (LR) without nested vertical subgraphs."""
        lines = [
            "---",
            "",
            "## 3. ROADMAP VISUAL DE MADUREZ (MERMAID LR OPTIMIZADO)",
            "",
            "Visualización de alta legibilidad en IDE con flujo horizontal continuo y codificación semántica de colores:",
            "",
            "```mermaid",
            "flowchart LR"
        ]

        # Render module cards
        for m in self.report.modules:
            node_id = m.module_id
            pct = f"{m.phase_completion_pct:.1f}%"
            status_label = "Done" if m.status == ModuleStatus.DONE else ("Active" if m.status == ModuleStatus.ACTIVE else "Backlog")

            # Clean name for Mermaid
            clean_name = m.name.replace('"', "'")
            label = f"\"<b>{m.module_id}: {clean_name}</b><br/>{pct} | {status_label}\""
            lines.append(f"    {node_id}[{label}]")

        lines.append("")

        # Sequential links from M01 to M10
        for i in range(len(self.report.modules) - 1):
            curr_mod = self.report.modules[i]
            next_mod = self.report.modules[i + 1]
            arrow = "-->" if next_mod.status in [ModuleStatus.DONE, ModuleStatus.ACTIVE] else "-.->"
            lines.append(f"    {curr_mod.module_id} {arrow} {next_mod.module_id}")

        lines.append("")

        # Summary node
        score_val = f"{self.report.consolidated_score:.1f}%"
        band_val = self.report.maturity_band.name
        clean_bottleneck = self.report.active_bottleneck.split("(")[0].strip().replace('"', "'")
        summary_label = f"\"<b>RESUMEN EJECUTIVO</b><br/>Score: {score_val} | {band_val}<br/>Cuello de Botella: {clean_bottleneck}\""
        lines.append(f"    SUMMARY[{summary_label}]")
        lines.append("    M10 ==> SUMMARY")
        lines.append("")

        # Styles
        lines.append("    %% Estilos semánticos")
        lines.append("    classDef done fill:#1E4620,stroke:#2ECC71,stroke-width:2px,color:#FFFFFF;")
        lines.append("    classDef active fill:#0D47A1,stroke:#2196F3,stroke-width:3px,color:#FFFFFF;")
        lines.append("    classDef backlog fill:#2C3E50,stroke:#7F8C8D,stroke-width:1px,stroke-dasharray: 4 4,color:#BDC3C7;")
        lines.append("    classDef blocked fill:#641E16,stroke:#E74C3C,stroke-width:2px,color:#FFFFFF;")
        lines.append("    classDef summary fill:#1A252F,stroke:#F39C12,stroke-width:2px,color:#F1C40F;")
        lines.append("")

        # Assign classes
        for m in self.report.modules:
            lines.append(f"    class {m.module_id} {m.status.value};")
        lines.append("    class SUMMARY summary;")

        lines.append("```")
        lines.append("")
        lines.append("**Leyenda Semántica:** `🟢 Verde (#1E4620 / #2ECC71)` = Done (100%) | `🔵 Azul (#0D47A1 / #2196F3)` = Active (1-99%) | `⚪ Gris (#2C3E50 / #7F8C8D)` = Backlog (0%) | `🔴 Rojo (#641E16 / #E74C3C)` = Blocked")

        return "\n".join(lines)

    def _render_forensic_breakdown(self) -> str:
        lines = [
            "---",
            "",
            "## 4. DESGLOSE FORENSE DE EVIDENCIAS POR MÓDULO",
            ""
        ]

        for m in self.report.modules:
            status_text = "🟢 DONE" if m.status == ModuleStatus.DONE else (
                "🔵 ACTIVE" if m.status == ModuleStatus.ACTIVE else "⚪ BACKLOG"
            )
            lines.append(f"### {m.module_id}: {m.name} — {status_text} ({m.phase_completion_pct:.1f}%)")
            lines.append(f"**Peso Relativo:** {m.weight*100:.0f}% | **Contribución Ponderada:** {m.weighted_contribution_pct:.2f}%")
            lines.append("")
            lines.append("| Criterio | Nombre | Estado | Evidencia Física Detectada |")
            lines.append("|:---|:---|:---:|:---|")

            for crit in m.criteria:
                status_badge = "✅ `[CUMPLIDO]`" if crit.fulfilled else "❌ `[FALTANTE]`"
                evidence_info = crit.evidence_detail
                if crit.evidence_path:
                    evidence_info = f"**`{crit.evidence_path}`** — {crit.evidence_detail}"
                lines.append(f"| `{crit.criterion_id}` | {crit.name} | {status_badge} | {evidence_info} |")

            lines.append("")

        return "\n".join(lines)

    def _render_remediation_plan(self) -> str:
        lines = [
            "---",
            "",
            "## 5. PLAN DE REMEDIACIÓN TÉCNICA PRIORIZADO (PATH TO 100%)",
            ""
        ]

        if not self.report.remediation_plan:
            lines.append("🎉 **¡Excelencia Operativa Alcanzada!** No se detectaron brechas técnicas pendientes. Todos los módulos canónicos se encuentran al 100% de cumplimiento.")
            return "\n".join(lines)

        lines.append("A continuación se prescriben las acciones técnicas prioritarias para desbloquear el avance del proyecto y alcanzar la máxima calificación:")
        lines.append("")
        lines.append("| Prioridad | Módulo | Criterio | Acción Requerida | Impacto Potencial | Archivos Sugeridos |")
        lines.append("|:---:|:---:|:---|:---|:---:|:---|")

        for item in self.report.remediation_plan:
            p_badge = f"**{item.priority}**"
            files_str = ", ".join(f"`{f}`" for f in item.files_to_touch) if item.files_to_touch else "—"
            lines.append(
                f"| {p_badge} | `{item.module_id}` | `{item.criterion_id}` | {item.action} | **+{item.impact_score:.2f}%** | {files_str} |"
            )

        return "\n".join(lines)


    def _render_spectral_context_efficiency(self) -> str:
        if not self.report.fpai:
            return ""
        fpai = self.report.fpai
        lines = [
            "---",
            "",
            "## 6. EFICIENCIA CONTEXTUAL Y VECTOR ESPECTRAL (FPAI ECONOMY)",
            "",
            "Métrica canónica de densidad cognitiva y preservación de potencia activa $P$:",
            "",
            "| Componente de Potencia | Símbolo | Tokens | Ratio | Estado |",
            "|:---|:---:|:---:|:---:|:---|",
            f"| **Potencia Activa** (Working Set) | $P$ | `{fpai.p_active:.0f}` | `{fpai.active_ratio:.1%}` | 🟢 Preservada |",
            f"| **Potencia Reactiva Inerte** | $Q_{{dead}}$ | `{fpai.q_dead:.0f}` | `{fpai.dead_ratio:.1%}` | ⚪ Inerte |",
            f"| **Potencia Reactiva Redundante** | $Q_{{dup}}$ | `{fpai.q_dup:.0f}` | `{fpai.redundant_ratio:.1%}` | 🟡 Duplicada |",
            f"| **Distorsión Estructural** | $D$ | `{fpai.d_structural:.0f}` | `{fpai.distortion_ratio:.1%}` | 🔴 Conflicto |",
            f"| **Potencia Aparente Espectral** | $S_{{spectral}}$ | `{fpai.s_spectral:.0f}` | — | $\\sqrt{{P^2 + Q^2 + D^2}}$ |",
            f"| **Potencia Aparente Lineal** | $S_{{linear}}$ | `{fpai.s_linear:.0f}` | — | $P + Q + D$ |",
            "",
            f"- **Factor de Potencia Espectral ($PF_{{spectral}}$):** `{fpai.power_factor_spectral:.3f}` *(Meta >= 0.70)*",
            f"- **Factor de Potencia Lineal ($PF_{{linear}}$):** `{fpai.power_factor_linear:.3f}`",
            f"- **Ratio de Divergencia Espectral:** `{fpai.divergence_ratio:.1%}`",
            f"- **Estado de Calibración:** `{fpai.calibration_state}` (Ganancia $G={fpai.gain_coefficient:.2f}$)",
        ]
        return "\n".join(lines)

    def _render_security_and_attack_surface(self) -> str:
        if not self.report.security:
            return ""
        sec = self.report.security
        badge_surf = "🟢 BAJA" if sec.attack_surface_index <= 15.0 else ("🟡 MEDIA" if sec.attack_surface_index <= 40.0 else "🔴 CRÍTICA")
        badge_ent = "🟢 ÓPTIMA" if sec.shannon_entropy_max <= 4.5 else "🔴 ALERTA"
        badge_pii = "🟢 CERO" if sec.pii_matches_count == 0 else "🔴 VIOLACIÓN"
        badge_inj = "🟢 INMUNE" if sec.prompt_injection_surface_count == 0 else "🔴 DETECTADA"
        badge_lock = "🟢 FIJADO" if sec.supply_chain_lockfile_pinned else "🔴 NO FIJADO"

        lines = [
            "---",
            "",
            "## 7. VECTOR DE SEGURIDAD Y SUPERFICIE DE ATAQUE AGÉNTICA",
            "",
            "Auditoría Zero-Tolerance de credenciales expuestas, entropía de Shannon e inyecciones:",
            "",
            "| Métrica de Seguridad | Valor Registrado | Umbral de Alerta | Estado |",
            "|:---|:---:|:---:|:---:|",
            f"| **Índice de Superficie de Ataque** | `{sec.attack_surface_index:.1f} / 100` | `<= 15.0` | {badge_surf} |",
            f"| **Entropía de Shannon Máxima ($H$)** | `{sec.shannon_entropy_max:.2f}` bits | `<= 4.50` | {badge_ent} |",
            f"| **Coincidencias PII (Zero-Tolerance)** | `{sec.pii_matches_count}` | `0` | {badge_pii} |",
            f"| **Inyecciones de Prompt Detectadas** | `{sec.prompt_injection_surface_count}` | `0` | {badge_inj} |",
            f"| **Pinning de Lockfile (Supply Chain)** | `{'Sí' if sec.supply_chain_lockfile_pinned else 'No'}` | `Requerido` | {badge_lock} |",
        ]
        return "\n".join(lines)

    def _render_systems_modularity_and_resilience(self) -> str:
        if not self.report.resilience:
            return ""
        res = self.report.resilience
        spof_str = ", ".join(res.spof_nodes) if res.spof_nodes else "Ninguno"
        lines = [
            "---",
            "",
            "## 8. VECTOR DE RESILIENCIA Y ACOPLAMIENTO DE SISTEMAS",
            "",
            "Análisis estático de estabilidad modular $I = \\frac{{C_e}}{{C_a + C_e}}$ y puntos únicos de fallo (SPOFs):",
            "",
            f"- **Módulos Analizados:** `{len(res.instability_i)}`",
            f"- **Puntos Únicos de Fallo (SPOFs) Detectados:** `{len(res.spof_nodes)}` ({spof_str})",
            f"- **Cobertura de Patrones de Tolerancia a Fallos:** `{res.resilience_coverage_ratio:.1%}`",
            "- **Recuento de Patrones Resilientes:**",
            f"  - Timeouts: `{res.resilience_patterns_count.get('timeout', 0)}`",
            f"  - Retries / Backoffs: `{res.resilience_patterns_count.get('retry', 0)}`",
            f"  - Circuit Breakers: `{res.resilience_patterns_count.get('circuit_breaker', 0)}`",
            f"  - Fallbacks: `{res.resilience_patterns_count.get('fallback', 0)}`",
        ]
        return "\n".join(lines)

    def _render_footer(self) -> str:
        return """---

> *Reporte generado automáticamente por **MetricsThinking™ Universal Project Auditor**.*  
> *Disciplina de auditoría: **Ground Truth First** (evidencia física sobre supuestos).*"""

