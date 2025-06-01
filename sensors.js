function loadData() {
  fetch("sensors.json")
    .then(response => response.json())
    .then(data => {
      console.log("Loaded sensor data:", data);
      document.body.append(JSON.stringify(data, null, 2));
    });
  setTimeout(() => location.reload(), 20000);
}
