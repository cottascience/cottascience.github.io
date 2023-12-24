input_file = "index.html"
output_file = "index.html"

# Read the content of the HTML file
with open(input_file, 'r') as file:
    html_content = file.read()

modified_content = html_content.replace( '.page-header-icon {\n\tfont-size: 3rem;', '.page-header-icon {\n\tfont-size: 8rem;'  )
modified_content = modified_content.replace('details open=', 'details close=')

# Write the modified content to a new file
with open(output_file, 'w') as file:
    file.write(modified_content)

print(f"CSS rule has been modified. Check {output_file}.")
