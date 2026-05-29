"use client";

import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import { API_BASE_URL } from "../lib/api";

export default function MapPage() {
  const mapContainer = useRef<HTMLDivElement | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!mapContainer.current) return;
    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          raster: {
            type: "raster",
            tiles: [process.env.NEXT_PUBLIC_MAP_TILE_URL || "https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
          },
        },
        layers: [
          {
            id: "raster",
            type: "raster",
            source: "raster",
          },
        ],
      },
      center: [30, 50],
      zoom: 4,
    });

    fetch(`${API_BASE_URL}/api/v1/events.geojson`)
      .then((res) => res.json())
      .then((data) => {
        if (!data.features) {
          setError("No event features loaded.");
          return;
        }
        map.on("load", () => {
          map.addSource("events", {
            type: "geojson",
            data,
          });
          map.addLayer({
            id: "event-points",
            type: "circle",
            source: "events",
            paint: {
              "circle-radius": 6,
              "circle-color": "#b91c1c",
              "circle-stroke-width": 1,
              "circle-stroke-color": "#fff",
            },
          });
        });
      })
      .catch(() => setError("Failed to load event geojson."));

    return () => map.remove();
  }, []);

  return (
    <main className="page">
      <header className="page-header">
        <h1>Map</h1>
        <p>MapLibre renders event points from the backend GeoJSON endpoint. The map remains empty until verified records include coordinates.</p>
      </header>
      <section className="panel" style={{ marginBottom: "16px" }}>
        <div className="filter-grid">
          <label>Category<select defaultValue=""><option value="">All categories</option><option value="air_attack">Air attack</option><option value="shelling">Shelling</option><option value="infrastructure_damage">Infrastructure damage</option></select></label>
          <label>Verification<select defaultValue=""><option value="">All statuses</option><option value="reported">Reported</option><option value="probable">Probable</option><option value="confirmed">Confirmed</option><option value="disputed">Disputed</option></select></label>
          <label>Location precision<select defaultValue=""><option value="">Any precision</option><option value="exact">Exact</option><option value="city">City</option><option value="oblast">Oblast</option></select></label>
        </div>
      </section>
      {error ? <div className="panel empty-state">{error}</div> : <div ref={mapContainer} className="map-canvas" />}
    </main>
  );
}
