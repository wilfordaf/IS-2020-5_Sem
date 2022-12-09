$count = 0
try {
    while ($true) {
        $count++
        $file = [io.file]::Create("E:\${count}.txt")
        $file.SetLength(1mb)
        $file.Close()
    }
} catch {    
    $file.Close()    
    Write-Error "Disk is full"
}