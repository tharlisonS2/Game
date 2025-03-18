<?php

function printDirectoryStructure($dir, $outputFile, $prefix = "", $isLast = true, $ignoredPaths = []) {
    // Get list of files/directories excluding . and ..
    $files = array_diff(scandir($dir), array('.', '..'));
    
    // Filter out ignored paths
    $filesToProcess = array();
    foreach ($files as $file) {
        $path = "$dir/$file";
        $skipPath = false;
        
        foreach ($ignoredPaths as $ignorePath) {
            if (strpos($path, $ignorePath) === 0) {
                $skipPath = true;
                break;
            }
        }
        
        if (!$skipPath) {
            $filesToProcess[] = $file;
        }
    }
    
    // Count how many elements we'll process
    $count = count($filesToProcess);
    
    // Process each file/directory
    $i = 0;
    foreach ($filesToProcess as $file) {
        $i++;
        $isCurrentLast = ($i === $count);
        $path = "$dir/$file";
        
        // Determine the connector and next prefix
        $connector = $isCurrentLast ? "└── " : "├── ";
        $nextPrefix = $prefix . ($isCurrentLast ? "    " : "│   ");
        
        // Write the current item to the output file
        file_put_contents($outputFile, "$prefix$connector$file\n", FILE_APPEND);
        
        // If it's a directory, recursively process it
        if (is_dir($path)) {
            printDirectoryStructure($path, $outputFile, $nextPrefix, $isCurrentLast, $ignoredPaths);
        }
    }
}

// Configuration
$outputFile = "directory_structure.txt";
$rootDir = "battle_arena"; // Root project directory
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
file_put_contents($outputFile, "Directory Structure for $rootDir\n");
file_put_contents($outputFile, str_repeat("=", 40) . "\n\n");

// Add the root directory and start scanning
file_put_contents($outputFile, "$rootDir\n", FILE_APPEND);
printDirectoryStructure($rootDir, $outputFile, "", true, $ignoredPaths);

echo "Directory structure has been written to $outputFile.";