const defaultZoom = 10;
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
  minZoom: 10,
  maxZoom: 18,
  maxBounds: maxBounds
});

const zoomDiv = document.getElementById('zoom');
map.on('zoom', () => {
  zoomDiv.innerHTML = 'Zoom : ' + map.getZoom().toFixed(2);
});

let lastZoom = map.getZoom();

map.on('zoomend', () => {
  const currentZoom = map.getZoom();
  const zoomDifference = currentZoom - lastZoom;

  if (zoomDifference >= 2) {
    console.log(zoomDifference);
  }

  lastZoom = currentZoom;
});