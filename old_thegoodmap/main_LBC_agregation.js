const defaultZoom = 10;
const mapCenter = [0, 43.5]; // Centre dans ta zone

const maxBounds = [
  [-1.25, 43], // [minLon, minLat]
  [0.9, 43.9]  // [maxLon, maxLat]
];

const sourceBounds = [-1.25, 43, 0.9, 43.9]; // emprise des données

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {

      lbc: {
        type: 'raster',
        tiles: [
          "https://lostinzoom.huma-num.fr/geoserver/gwc/service/tms/1.0.0/la_bonne_carte:LBC_agregation@WebMercatorQuad@png/{z}/{x}/{y}.png"
        ],
        tileSize: 256,
        scheme: "tms",          // Geoserver fournit du TMS
        bounds: sourceBounds,   // emprise exacte des données
        minzoom: 9,
        maxzoom: 18
      }
    },
    layers: [
      {
        id: 'lbc-layer',
        type: 'raster',
        source: 'lbc',
        minzoom: 9,
        maxzoom: 18
      }
    ]
  },
  center: mapCenter,
  zoom: defaultZoom,
  minZoom: 9,
  maxZoom: 18,
  maxBounds: maxBounds
});

// Affichage du zoom courant
const zoomDiv = document.getElementById('zoom');
map.on('zoom', () => {
  zoomDiv.innerHTML = 'Zoom : ' + map.getZoom().toFixed(2);
});

