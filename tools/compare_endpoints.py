import re, sys, json, yaml, csv
from pathlib import Path

METHODS = {"GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD"}

# Excluir cosas auxiliares
EXCLUDE_PREFIXES = ("/admin", "/__debug__", "/static", "/media")
EXCLUDE_EXACT = {"/", "/api"}         # ignorar raíz del router
EXCLUDE_REGEX = [r"/i18n"]

def norm_path(p: str) -> str:
    if not p:
        return p
    # quitar espacios raros
    p = re.sub(r"\s+", "", p)
    # quitar anchors de regex
    p = p.strip().replace("^", "").replace("$", "")
    # quitar TODAS las variantes de formato:
    #   "\.{format}", ".{format}", con/sin barra al final
    p = re.sub(r"(\\)?\.\{format\}(/)?", "", p)
    # quitar capturas (?P<format>...) si aparecieran
    p = re.sub(r"\(\?P<format>[^)]+\)", "", p)
    # normalizar parámetros a {param}
    p = re.sub(r"\(\?P<([^>]+)>[^)]+\)", r"{\1}", p)  # (?P<id>[^/]+) -> {id}
    p = re.sub(r"<[^:>]+:([^>]+)>", r"{\1}", p)       # <int:id> -> {id}
    p = re.sub(r"<([^>]+)>", r"{\1}", p)              # <id> -> {id}
    # asegurar slash inicial, sin duplicados ni trailing
    if not p.startswith("/"):
        p = "/" + p
    p = re.sub(r"/{2,}", "/", p)
    if len(p) > 1 and p.endswith("/"):
        p = p[:-1]
    return p

def should_exclude(path: str) -> bool:
    if path in EXCLUDE_EXACT:
        return True
    if "{format}" in path:
        return True
    if path.startswith(EXCLUDE_PREFIXES):
        return True
    for rx in EXCLUDE_REGEX:
        if re.search(rx, path):
            return True
    return False

def parse_urls_json(path: Path):
    # tolerante a UTF-8 y UTF-16 de PowerShell
    data = None
    for enc in ("utf-8", "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            data = json.loads(path.read_text(encoding=enc))
            break
        except Exception:
            data = None
    if data is None:
        raise RuntimeError(f"No pude leer {path}. Re-generá con: python manage.py show_urls --format=json | Out-File -Encoding utf8 .\\urls.json")

    entries = {}
    for row in data:
        url = row.get("url") or row.get("pattern") or ""
        m = (row.get("method") or "").upper()
        p = norm_path(url)
        if should_exclude(p):
            continue
        entries.setdefault(p, set())
        if m in METHODS:
            entries[p].add(m)
    return entries

def parse_urls_txt(path: Path):
    entries = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.search(r'(/.*)$', line.strip())
        url_raw = m.group(1) if m else ""
        p = norm_path(url_raw)
        if should_exclude(p):
            continue
        entries.setdefault(p, set()).add("GET")
    return entries

def parse_openapi(path: Path):
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    result = {}
    for p, ops in (spec.get("paths") or {}).items():
        pn = norm_path(p)
        if should_exclude(pn):
            continue
        for m, _op in (ops or {}).items():
            ml = m.upper()
            if ml in METHODS:
                result.setdefault(pn, set()).add(ml)
    return result

def write_csv(rows, out_path: Path, headers):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(headers); w.writerows(rows)

def main(urls_file, openapi_file):
    urls_path = Path(urls_file); oa_path = Path(openapi_file)
    base_out = Path("endpoint_diff"); base_out.mkdir(parents=True, exist_ok=True)

    if urls_path.suffix.lower() == ".json":
        urls_map = parse_urls_json(urls_path)
    else:
        urls_map = parse_urls_txt(urls_path)
    oa_map = parse_openapi(oa_path)

    only_urls = sorted([p for p in urls_map if p not in oa_map])
    only_oa = sorted([p for p in oa_map if p not in urls_map])

    md = []
    md.append("# Comparación de Endpoints (urls vs openapi)")
    md.append("## Resumen")
    md.append(f"- En URLs (limpio): **{len(urls_map)}** rutas")
    md.append(f"- En OpenAPI: **{len(oa_map)}** rutas")
    md.append(f"- Solo en URLs: **{len(only_urls)}**")
    md.append(f"- Solo en OpenAPI: **{len(only_oa)}**")
    md.append("")
    if only_urls:
        md.append("## Rutas solo en URLs")
        md.extend([f"- `{p}`" for p in only_urls])
        md.append("")
    if only_oa:
        md.append("## Rutas solo en OpenAPI")
        md.extend([f"- `{p}`" for p in only_oa])
        md.append("")

    (base_out / "comparison.md").write_text("\n".join(md), encoding="utf-8")
    write_csv([[p] for p in only_urls], base_out / "only_in_urls.csv", ["path"])
    write_csv([[p] for p in only_oa], base_out / "only_in_openapi.csv", ["path"])

    print("OK - Reportes en:", base_out.resolve())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python tools/compare_endpoints.py urls.json openapi.yaml")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])