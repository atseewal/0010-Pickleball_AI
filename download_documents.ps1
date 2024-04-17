# Destination Folder
$dest = ".\data\"

# Source URL - 2024
$url_2024_rules = "https://usapickleball.org/docs/USA-Pickleball-Official-Rulebook-2024-v1.pdf"
$dest_2024_rules = ($dest + "USA_Pickleball_Rulebook_2024_v1.pdf")

Write-Host $dest_2024_rules

Invoke-WebRequest -Uri $url_2024_rules -OutFile $dest_2024_rules