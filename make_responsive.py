import os
import glob
import re

def make_responsive():
    templates_dir = os.path.join("app", "templates")
    html_files = glob.glob(os.path.join(templates_dir, "*.html"))
    
    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # 1. Fix fixed heights to min-heights on mobile
        new_content = re.sub(r'h-\[400px\]', r'min-h-[300px] md:h-[400px]', new_content)
        new_content = re.sub(r'h-\[450px\]', r'min-h-[350px] md:h-[450px]', new_content)
        new_content = re.sub(r'h-\[500px\]', r'min-h-[350px] md:h-[500px]', new_content)
        new_content = re.sub(r'h-\[600px\]', r'min-h-[400px] md:h-[600px]', new_content)
        new_content = re.sub(r'h-screen', r'min-h-[calc(100vh-64px)] md:h-screen', new_content)

        # 2. Fix grids that might not be responsive
        # Replace grid-cols-4 with grid-cols-1 md:grid-cols-2 lg:grid-cols-4 if not already responsive
        new_content = re.sub(r'(?<!md:)(?<!lg:)(?<!xl:)grid-cols-4', r'grid-cols-1 md:grid-cols-2 lg:grid-cols-4', new_content)
        new_content = re.sub(r'(?<!md:)(?<!lg:)(?<!xl:)grid-cols-3', r'grid-cols-1 md:grid-cols-2 lg:grid-cols-3', new_content)
        new_content = re.sub(r'(?<!md:)(?<!lg:)(?<!xl:)grid-cols-2', r'grid-cols-1 md:grid-cols-2', new_content)

        # 3. Ensure flex items wrap or change to column on mobile
        new_content = re.sub(r'flex justify-between items-center', r'flex flex-col md:flex-row md:justify-between md:items-center gap-4', new_content)
        
        # We need to make sure we don't break things that already have flex-col
        # Let's be careful with regex on flex
        
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Made responsive {file_path}")
        else:
            print(f"No changes needed for {file_path}")

if __name__ == "__main__":
    make_responsive()
