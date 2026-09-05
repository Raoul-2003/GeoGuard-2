import sys

content = open('d:/GeoGuard/src/download_sentinel2.py', encoding='utf-8').read()

content = content.replace('AOI_FILE = Path("data/aoi/aoi_abidjan.geojson")', 'AOI_FILE = Path(__file__).parent.parent / "data/aoi/aoi_abidjan.geojson"')
content = content.replace('OUTPUT_DIR = Path("data/raw/sentinel2")', 'OUTPUT_DIR = Path(__file__).parent.parent / "data/raw/sentinel2"')

lines = content.split('\n')
new_lines = []
in_function = False
for line in lines:
    if line.startswith('print("=" * 70)') and not in_function:
        new_lines.append('def run_download(product_id=PRODUCT_ID):')
        new_lines.append('    try:')
        in_function = True
    
    if in_function:
        if line == '    ids=[PRODUCT_ID]':
            new_lines.append('        ids=[product_id]')
        else:
            new_lines.append('        ' + line)
    else:
        new_lines.append(line)

new_lines.append('    except Exception as e:')
new_lines.append('        print(f"Erreur lors du téléchargement: {e}")')
new_lines.append('        return False')
new_lines.append('    return True')
new_lines.append('')
new_lines.append('if __name__ == "__main__":')
new_lines.append('    run_download()')

open('d:/GeoGuard/src/download_sentinel2.py', 'w', encoding='utf-8').write('\n'.join(new_lines))
