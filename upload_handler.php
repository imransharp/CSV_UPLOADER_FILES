<?php
date_default_timezone_set('Asia/Karachi');
set_time_limit(0); 
include 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $table = $_POST['target_table'];
    $file = $_FILES['csv_file'];

    // Check file
    if ($file['error'] !== UPLOAD_ERR_OK) {
        die("File upload error");
    }

    $filename = basename($file['name']);
    $target_path = "uploads/" . $filename;

    // Move to uploads folder
    if (!move_uploaded_file($file['tmp_name'], $target_path)) {
        die("Failed to move uploaded file");
    }
    
    // Backup the table    
    $backup_table = $table . "_backup";

    // 1) Ensure the backup table exists
    $conn->query("CREATE TABLE IF NOT EXISTS `$backup_table` LIKE `$table`");

    // 2) Clear out the old backup
    $conn->query("TRUNCATE TABLE `$backup_table`");

    // 3) Copy current data for safekeeping
    $conn->query("INSERT INTO `$backup_table` SELECT * FROM `$table`");

    // $backup_table = $table . "_backup_" . date("Ymd_His");
    // $conn->query("CREATE TABLE $backup_table AS SELECT * FROM $table");

    // 🧹 Clear the existing data
    $conn->query("TRUNCATE TABLE $table");
     
    // Start DB transaction
    $conn->begin_transaction();

    try 
    {
        $handle = fopen($target_path, "r");
        if (!$handle) throw new Exception("Cannot open CSV");

        fgetcsv($handle); // Skip header

        $batchSize = 1000;
        $rowCount = 0;
        $batch = [];

        while (($row = fgetcsv($handle)) !== FALSE) {
            $escaped = array_map(fn($val) => "'" . $conn->real_escape_string($val) . "'", $row);
            $batch[] = "(" . implode(",", $escaped) . ")";
            $rowCount++;

            if ($rowCount % $batchSize === 0) {
                $sql = "INSERT INTO $table VALUES " . implode(",", $batch);
                $conn->query($sql);
                $batch = []; // reset
            }
        }

        // Insert remaining rows
        if (count($batch) > 0) {
            $sql = "INSERT INTO $table VALUES " . implode(",", $batch);
            $conn->query($sql);
        }

        fclose($handle);
        $conn->commit();
        // echo "✅ Upload complete: $rowCount rows inserted.";
        // After success
        // header("Location: index.php?status=success");
        // exit;
        // $rowCount = $number_of_rows_uploaded; // Replace with actual count
        $logFile = "upload_logs.txt";
        $logMsg = "[" . date("Y-m-d H:i:s") . "] Uploaded to table: $table, Rows: $rowCount, Status: success\n";
        file_put_contents($logFile, $logMsg, FILE_APPEND);

        header("Location: index.php?status=success&rows=$rowCount");
        exit;
            
    } catch (Exception $e) {
        $conn->rollback();
        // echo "❌ Upload failed: " . $e->getMessage();
          // Or after failure
        $logMsg = "[" . date("Y-m-d H:i:s") . "] Upload to table: $table failed.\n";
        file_put_contents($logFile, $logMsg, FILE_APPEND);

        header("Location: index.php?status=fail");
        exit;
    }       

    $conn->close();
} else {
    echo "Invalid request";
}
?>
