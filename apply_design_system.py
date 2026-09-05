import os
import glob
import re

# Dictionary of replacements
replacements = {
    # Backgrounds
    "bg-surface-container-lowest": "bg-white",
    "bg-surface-container": "bg-gray-50",
    "bg-surface/50": "bg-gray-50/50",
    "bg-surface": "bg-white",
    
    # Text colors
    "text-on-surface-variant": "text-text-muted",
    "text-on-surface": "text-text-main",
    
    # Borders
    "border-outline-variant": "border-gray-200",
    "border-outline": "border-gray-200",
    
    # Primary/Secondary/Error mapping
    "text-error": "text-critical",
    "bg-error": "bg-critical",
    "border-error/20": "border-critical/20",
    "border-error/30": "border-critical/30",
    
    "text-[#f59e0b]": "text-medium",
    "bg-[#f59e0b]": "bg-medium",
    "bg-[#f59e0b]/10": "bg-medium/10",
    
    "bg-secondary": "bg-white",
    "text-on-secondary": "text-text-main",
    "hover:bg-secondary-container": "hover:bg-gray-50",
    
    # Spacing and layout (approximations for standard buttons and cards)
    "rounded-xl": "rounded-2xl", # 16px
    "rounded-lg": "rounded-[10px]", # 10px
    
    # Table headers
    "bg-surface border-b": "bg-gray-50 border-b",
}

def apply_design_system():
    # Find all html files in app/templates
    templates_dir = os.path.join("app", "templates")
    html_files = glob.glob(os.path.join(templates_dir, "*.html"))
    
    for file_path in html_files:
        if "base.html" in file_path:
            continue # We already did base.html manually
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # Apply strict string replacements
        for old_str, new_str in replacements.items():
            new_content = new_content.replace(old_str, new_str)
            
        # Specific fix for secondary buttons (which we turned to bg-white, they need borders)
        # Instead of complex regex, let's just let Tailwind class aggregation handle it
        
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes for {file_path}")

if __name__ == "__main__":
    apply_design_system()
