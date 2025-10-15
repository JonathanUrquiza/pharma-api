# tools/openapi_to_md.py
import sys, json, yaml, os
from collections import defaultdict

def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".json"):
            return json.load(f)
        return yaml.safe_load(f)

def fmt_schema(schema):
    if not schema: return "-"
    t = schema.get("type")
    ref = schema.get("$ref")
    if ref: return ref.split("/")[-1]
    if t == "array":
        items = schema.get("items", {})
        return f"array<{fmt_schema(items)}>"
    if t == "object":
        props = schema.get("properties", {})
        keys = ", ".join(list(props.keys())[:6])
        return f"object{{{keys}{'…' if len(props)>6 else ''}}}"
    return t or "-"

def get_auth(spec):
    sa = spec.get("security", [])
    if not sa: return "—"
    parts=[]
    for req in sa:
        for name, scopes in req.items():
            parts.append(f"{name}({','.join(scopes)})" if scopes else name)
    return "; ".join(parts) or "—"

def md_escape(s): return (s or "").replace("|", "\\|").replace("\n", " ").strip()

def main(in_file, out_file, apis_csv=None):
    spec = load_spec(in_file)
    title = spec.get("info", {}).get("title", "API")
    version = spec.get("info", {}).get("version", "")
    servers = [s.get("url","") for s in spec.get("servers", [])]
    base_urls = ", ".join(servers) if servers else "—"
    global_auth = get_auth(spec)

    lines=[]
    lines.append(f"# {title} – Endpoints (v{version})")
    lines.append("")
    lines.append(f"- **Base URLs**: {base_urls}")
    lines.append(f"- **Autenticación global**: {global_auth}")
    lines.append("")
    lines.append("## Matriz de Endpoints")
    lines.append("| Método | Ruta | operationId | Descripción | Auth | Consumes | Produces |")
    lines.append("|---|---|---|---|---|---|---|")

    paths = spec.get("paths", {})
    for path, ops in sorted(paths.items()):
        for method, op in ops.items():
            if method.lower() not in {"get","post","put","patch","delete","options","head"}:
                continue
            opid = op.get("operationId","—")
            desc = op.get("summary") or op.get("description") or "—"
            # auth por operación o hereda global
            op_auth = "—"
            if "security" in op:
                op_auth = "; ".join([f"{k}({','.join(v)})" if v else k for d in op["security"] for k,v in d.items()]) or "—"
            else:
                op_auth = global_auth

            # mime types
            consumes = ", ".join(op.get("requestBody",{}).get("content",{}).keys()) or "—"
            produces = ", ".join(op.get("responses",{}).get("200",{}).get("content",{}).keys()) or "—"

            lines.append(f"| {method.upper()} | `{path}` | {md_escape(opid)} | {md_escape(desc)} | {md_escape(op_auth)} | {md_escape(consumes)} | {md_escape(produces)} |")

    # Detalle por endpoint
    lines.append("\n## Detalle por Endpoint")
    for path, ops in sorted(paths.items()):
        lines.append(f"\n### `{path}`")
        for method, op in ops.items():
            if method.lower() not in {"get","post","put","patch","delete","options","head"}:
                continue
            lines.append(f"\n#### {method.upper()}")
            lines.append(f"- **operationId**: `{op.get('operationId','—')}`")
            lines.append(f"- **Resumen**: {md_escape(op.get('summary') or op.get('description') or '—')}")
            # parámetros
            params = op.get("parameters", [])
            if params:
                lines.append("**Parámetros**:")
                lines.append("| En | Nombre | Tipo | Requerido | Descripción |")
                lines.append("|---|---|---|---|---|")
                for p in params:
                    schema = p.get("schema", {})
                    lines.append(f"| {p.get('in','-')} | {p.get('name','-')} | {fmt_schema(schema)} | {p.get('required',False)} | {md_escape(p.get('description','-'))} |")
            else:
                lines.append("_Sin parámetros_")

            # requestBody
            rb = op.get("requestBody")
            if rb:
                lines.append("**Request Body**:")
                for mt, media in rb.get("content", {}).items():
                    schema = media.get("schema", {})
                    lines.append(f"- {mt}: `{fmt_schema(schema)}`")

            # responses
            lines.append("**Responses**:")
            resps = op.get("responses", {})
            for code, r in sorted(resps.items()):
                mt = ", ".join(r.get("content",{}).keys()) or "—"
                lines.append(f"- {code}: {md_escape(r.get('description','')) or '—'} (content: {mt})")

    # Sección de reglas de negocio (plantilla)
    lines.append("""
## Reglas de Negocio (Farmacia)
- Validación EAN-13 y GS1 DataMatrix (rechazo si checksum inválido).
- Prohibición de stock negativo (HTTP 409 al intentar dejar stock < 0).
- FEFO (First-Expire, First-Out) para ventas/salidas.
- Bloqueo automático de productos vencidos.
- Trazabilidad: todos los movimientos generan registro de auditoría (usuario, timestamp, antes/después, motivo).
""")

    # APIs externas (si nos pasan el CSV)
    if apis_csv and os.path.exists(apis_csv):
        lines.append("\n## APIs Externas Consumidas\n")
        lines.append(f"_Fuente: {apis_csv}_  \n")
        try:
            import csv
            lines.append("| Nombre | Base URL | Endpoints | Auth | Scopes | Rate limit | Timeouts | Retries | Contacto/Docs |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            with open(apis_csv, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    lines.append("| " + " | ".join(md_escape(row.get(k,"")) for k in
                                   ["Nombre","BaseURL","EndpointsUsados","Autenticacion","Scopes","RateLimit","Timeouts","Retries","Contacto/Docs"]) + " |")
        except Exception as e:
            lines.append(f"_No se pudo leer el CSV: {e}_")

    os.makedirs("docs", exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generado: {out_file}")

if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "openapi.yaml"
    apis_csv = sys.argv[2] if len(sys.argv) > 2 else None
    out_file = "docs/ENDPOINTS.md"
    main(in_file, out_file, apis_csv)
