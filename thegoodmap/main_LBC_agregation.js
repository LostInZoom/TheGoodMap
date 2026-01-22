const defaultZoom = 9;
const mapCenter = [0, 43.5]; 

const maxBounds = [
  [-1.25, 43], // [minLon, minLat]
  [0.9, 43.9]  // [maxLon, maxLat]
];


const map = new maplibregl.Map({
  container: 'map',
  style: './style.json',
  center: mapCenter,
  zoom: defaultZoom,
  minZoom: 8,
  maxZoom: 18,
  maxBounds: maxBounds
});

const zoomDiv = document.getElementById('zoom');

map.on('zoom', () => {
  const zRaw = map.getZoom();

  zoomDiv.innerHTML = `
    Zoom MapLibre : ${zRaw.toFixed(2)}<br>
  `;
});





