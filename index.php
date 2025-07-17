<?php
$tables = ['accts_sub', 'accts_chg', 'accts_dis', 'accts_dor', 'accts_gcr','accts_pay','accts_rev','mtd'];
?>
<!DOCTYPE html>
<html>
<head>
  <title>BI CSV Uploader</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

</head>
<body class="bg-light">

<div class="container mt-5">
  <div class="card shadow rounded-4 p-4">
    <h2 class="mb-4">📤 Upload CSV</h2>

  <!-- ✅ Status Alert Block -->
    <?php if (isset($_GET['status']) && $_GET['status'] === 'success'): ?>
      <div class="alert alert-success">✅ Upload Successful!
        <?php if (isset($_GET['rows'])): ?>
          <br>Inserted Rows: <strong><?= htmlspecialchars($_GET['rows']) ?></strong>
        <?php endif; ?>
      </div>
    <?php elseif (isset($_GET['status']) && $_GET['status'] === 'fail'): ?>
      <div class="alert alert-danger">❌ Upload Failed.</div>
    <?php endif; ?>

    <!-- ✅ End Alert Block -->
    <form action="upload_handler.php" method="POST" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="target_table" class="form-label">Select Table</label>
        <select name="target_table" id="target_table" class="form-select" required>
          <?php foreach ($tables as $table): ?>
            <option value="<?= $table ?>"><?= $table ?></option>
          <?php endforeach; ?>
        </select>
      </div>

      <div class="mb-3">
        <label for="csv_file" class="form-label">Choose CSV File</label>
        <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
      </div>

      <button type="submit" class="btn btn-primary">Upload</button>

    </form>

    <div class="mt-5">
    <h5>📄 Upload Logs - Last 10</h5>
    <div class="border rounded bg-white p-3" style="max-height: 200px; overflow-y: auto; font-family: monospace; font-size: 0.9rem;">
      <?php
        $logPath = "upload_logs.txt";
        if (file_exists($logPath)) {
          $logs = array_slice(file($logPath), -10); // show last 10 logs
          foreach ($logs as $log) {
            echo htmlspecialchars($log) . "<br>";
          }
        } else {
          echo "No logs found.";
        }
      ?>
    </div>
   </div>

  </div>
</div>

<script>
    const form = document.querySelector("form");
    form.addEventListener("submit", () => {
      const btn = form.querySelector("button");
      btn.innerHTML = 'Uploading...';
      btn.disabled = true;
    });
</script>


</body>
</html>
