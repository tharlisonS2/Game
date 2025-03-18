<?php

function scanDirectory($dir, $outputFile, $allowedExtensions = [], $ignoredPaths = [], $rootDir = "") {
    $files = scandir($dir);
    
    foreach ($files as $file) {
        if ($file === '.' || $file === '..') {
            continue;
        }
        
        $filePath = "$dir/$file";
        
        // Skip ignored paths
        $skipFile = false;
        foreach ($ignoredPaths as $ignoredPath) {
            if (strpos($filePath, $ignoredPath) === 0) {
                $skipFile = true;
                break;
            }
        }
        
        if ($skipFile) {
            continue;
        }
        
        if (is_dir($filePath)) {
            scanDirectory($filePath, $outputFile, $allowedExtensions, $ignoredPaths, $rootDir);
        } elseif (is_file($filePath)) {
            $fileExtension = pathinfo($filePath, PATHINFO_EXTENSION);
            
            // Check if file extension is in allowed list
            if (!empty($allowedExtensions) && !in_array($fileExtension, $allowedExtensions)) {
                continue;
            }
            
            // Add only the absolute path as a comment
            file_put_contents($outputFile, "# $filePath\n", FILE_APPEND | LOCK_EX);
            
            // Read file content
            $content = @file_get_contents($filePath);
            if ($content === false) {
                file_put_contents($outputFile, "# ERROR: Could not read file content\n\n", FILE_APPEND | LOCK_EX);
                continue;
            }
            
            // Handle encoding issues
            $encodings = ['UTF-8', 'ASCII', 'ISO-8859-1', 'WINDOWS-1252'];
            $detected = mb_detect_encoding($content, $encodings, true);
            $cleanContent = $detected ? mb_convert_encoding($content, 'UTF-8', $detected) : utf8_encode($content);
            
            // Process content line by line to remove relative path comments
            $lines = explode("\n", $cleanContent);
            $filteredLines = [];
            $skipNextLine = false;
            
            foreach ($lines as $index => $line) {
                // Skip the first comment line if it's a relative path
                if ($index === 0 && preg_match('/^#\s+[\w\/\.]+$/', trim($line))) {
                    continue;
                }
                
                // Add the line to our filtered content
                $filteredLines[] = $line;
            }
            
            // Add filtered file content followed by separator
            $filteredContent = implode("\n", $filteredLines);
            file_put_contents($outputFile, $filteredContent . "\n\n", FILE_APPEND | LOCK_EX);
            file_put_contents($outputFile, "# " . str_repeat('-', 80) . "\n\n", FILE_APPEND | LOCK_EX);
        }
    }
}

// Configuration
$outputFile = "merged_output.txt";
$rootDir = "battle_arena"; // Root project directory
$allowedExtensions = ["py", "php", "txt"]; // Allowed file extensions
$ignoredPaths = [
    "battle_arena/__pycache__",
    "battle_arena/entities/__pycache__",
    "battle_arena/ui/__pycache__"
];

// Delete output file if it exists
if (file_exists($outputFile)) {
    unlink($outputFile);
}

// Start with a header in the output file
touch($outputFile);
file_put_contents($outputFile, "# Project Files Merger\n");
file_put_contents($outputFile, "# Generated on: " . date("Y-m-d H:i:s") . "\n");
file_put_contents($outputFile, "# Root directory: $rootDir\n");
file_put_contents($outputFile, "# " . str_repeat('=', 80) . "\n\n", FILE_APPEND | LOCK_EX);

// Start scanning
scanDirectory($rootDir, $outputFile, $allowedExtensions, $ignoredPaths, $rootDir);

echo "All files have been merged into $outputFile with absolute paths only.";