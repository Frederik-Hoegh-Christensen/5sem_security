# Define the ports for your servers
$Ports = @(8080, 8081, 8082, 8083)

# Define the server script filenames
$ServerScripts = @("alice.py", "bob.py", "charlie.py", "hospital.py")

# Get the current directory
$CurrentDir = Get-Location

# Loop through the servers and start them
foreach ($i in 0..($Ports.Length - 1)) {
    $Port = $Ports[$i]
    $Script = $ServerScripts[$i]

    
    # Start the server from the current directory
    Start-Process -FilePath "py" -ArgumentList "$Script", "$Port" -WorkingDirectory $CurrentDir

    # Sleep for a moment to allow the server to start before moving on
    Start-Sleep -Seconds 5
}