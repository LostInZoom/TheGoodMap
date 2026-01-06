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
  const zCorrected = correctedZoom(map);

  zoomDiv.innerHTML = `
    Zoom MapLibre : ${zRaw.toFixed(2)}<br>
    Zoom corrigé (OL / Google) : ${zCorrected.toFixed(2)}
  `;
});

let lastZoom = map.getZoom();


function correctedZoom(map) {
  const z = map.getZoom();
  const lat = map.getCenter().lat;

  const latRad = lat * Math.PI / 180;
  const correction = Math.log2(Math.cos(latRad));

  return z + correction;
}



