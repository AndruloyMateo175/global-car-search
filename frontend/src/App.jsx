import React, { useState } from 'react'

const API_BASE = '/api'

// ---- Styles ----
const styles = {
  app: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
    color: '#fff',
  },
  header: {
    textAlign: 'center',
    padding: '40px 20px 20px',
  },
  logo: {
    fontSize: '3rem',
    fontWeight: 800,
    background: 'linear-gradient(90deg, #00d2ff, #3a7bd5)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    margin: 0,
  },
  subtitle: {
    color: '#8892b0',
    fontSize: '1.1rem',
    marginTop: '8px',
  },
  searchBox: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '30px',
    background: 'rgba(255,255,255,0.05)',
    borderRadius: '16px',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255,255,255,0.1)',
  },
  inputRow: {
    display: 'flex',
    gap: '12px',
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  input: {
    padding: '14px 20px',
    fontSize: '1rem',
    borderRadius: '10px',
    border: '1px solid rgba(255,255,255,0.2)',
    background: 'rgba(255,255,255,0.08)',
    color: '#fff',
    outline: 'none',
    flex: '1',
    minWidth: '150px',
    transition: 'border 0.3s',
  },
  button: {
    padding: '14px 40px',
    fontSize: '1.1rem',
    fontWeight: 700,
    borderRadius: '10px',
    border: 'none',
    background: 'linear-gradient(90deg, #00d2ff, #3a7bd5)',
    color: '#fff',
    cursor: 'pointer',
    transition: 'transform 0.2s, opacity 0.2s',
    minWidth: '180px',
  },
  buttonDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed',
  },
  tabs: {
    display: 'flex',
    justifyContent: 'center',
    gap: '8px',
    marginTop: '30px',
    flexWrap: 'wrap',
  },
  tab: {
    padding: '10px 24px',
    borderRadius: '8px',
    border: '1px solid rgba(255,255,255,0.15)',
    background: 'transparent',
    color: '#8892b0',
    cursor: 'pointer',
    fontSize: '0.95rem',
    fontWeight: 600,
    transition: 'all 0.2s',
  },
  tabActive: {
    background: 'linear-gradient(90deg, #00d2ff, #3a7bd5)',
    color: '#fff',
    border: '1px solid transparent',
  },
  results: {
    maxWidth: '1000px',
    margin: '30px auto',
    padding: '0 20px',
  },
  card: {
    background: 'rgba(255,255,255,0.06)',
    borderRadius: '12px',
    padding: '20px',
    marginBottom: '12px',
    border: '1px solid rgba(255,255,255,0.08)',
    transition: 'transform 0.2s',
  },
  cardTitle: {
    fontSize: '1.1rem',
    fontWeight: 700,
    margin: '0 0 8px',
    color: '#e6f1ff',
  },
  cardMeta: {
    color: '#8892b0',
    fontSize: '0.9rem',
    margin: '4px 0',
  },
  link: {
    color: '#00d2ff',
    textDecoration: 'none',
    fontWeight: 600,
    display: 'inline-block',
    marginTop: '8px',
  },
  badge: {
    display: 'inline-block',
    padding: '3px 10px',
    borderRadius: '20px',
    fontSize: '0.75rem',
    fontWeight: 700,
    marginRight: '6px',
  },
  specGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '12px',
  },
  specItem: {
    background: 'rgba(255,255,255,0.04)',
    padding: '12px',
    borderRadius: '8px',
    border: '1px solid rgba(255,255,255,0.06)',
  },
  specLabel: {
    fontSize: '0.75rem',
    color: '#8892b0',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  specValue: {
    fontSize: '1.1rem',
    fontWeight: 700,
    color: '#e6f1ff',
    marginTop: '4px',
  },
  priceBar: {
    height: '24px',
    borderRadius: '6px',
    background: 'linear-gradient(90deg, #00d2ff, #3a7bd5)',
    transition: 'width 0.5s ease',
  },
  statsRow: {
    display: 'flex',
    gap: '20px',
    justifyContent: 'center',
    marginTop: '20px',
    flexWrap: 'wrap',
  },
  stat: {
    textAlign: 'center',
    padding: '16px 24px',
    background: 'rgba(255,255,255,0.05)',
    borderRadius: '12px',
    minWidth: '120px',
  },
  statNumber: {
    fontSize: '2rem',
    fontWeight: 800,
    background: 'linear-gradient(90deg, #00d2ff, #3a7bd5)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  statLabel: {
    color: '#8892b0',
    fontSize: '0.85rem',
    marginTop: '4px',
  },
  loader: {
    textAlign: 'center',
    padding: '60px',
  },
  spinner: {
    width: '50px',
    height: '50px',
    border: '4px solid rgba(255,255,255,0.1)',
    borderTop: '4px solid #00d2ff',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
    margin: '0 auto 20px',
  },
  footer: {
    textAlign: 'center',
    padding: '40px 20px',
    color: '#4a5568',
    fontSize: '0.85rem',
  },
  sourcesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
    gap: '10px',
    marginTop: '16px',
  },
  sourceChip: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 14px',
    background: 'rgba(255,255,255,0.04)',
    borderRadius: '8px',
    fontSize: '0.85rem',
    color: '#8892b0',
  },
}

const countryFlags = {
  EU: '\uD83C\uDDEA\uD83C\uDDFA', DE: '\uD83C\uDDE9\uD83C\uDDEA', US: '\uD83C\uDDFA\uD83C\uDDF8',
  GB: '\uD83C\uDDEC\uD83C\uDDE7', AR: '\uD83C\uDDE6\uD83C\uDDF7', MX: '\uD83C\uDDF2\uD83C\uDDFD',
  UY: '\uD83C\uDDFA\uD83C\uDDFE', CO: '\uD83C\uDDE8\uD83C\uDDF4', CL: '\uD83C\uDDE8\uD83C\uDDF1',
  BR: '\uD83C\uDDE7\uD83C\uDDF7', PE: '\uD83C\uDDF5\uD83C\uDDEA', EC: '\uD83C\uDDEA\uD83C\uDDE8',
  JP: '\uD83C\uDDEF\uD83C\uDDF5', ZA: '\uD83C\uDDFF\uD83C\uDDE6', AU: '\uD83C\uDDE6\uD83C\uDDFA',
  PL: '\uD83C\uDDF5\uD83C\uDDF1', AE: '\uD83C\uDDE6\uD83C\uDDEA', LATAM: '\uD83C\uDF0E',
  GLOBAL: '\uD83C\uDF10',
}

function App() {
  const [make, setMake] = useState('')
  const [model, setModel] = useState('')
  const [year, setYear] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('listings')

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!make || !model) return

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const params = new URLSearchParams({ make, model })
      if (year) params.append('year', year)

      const resp = await fetch(`${API_BASE}/search/?${params}`)
      if (!resp.ok) throw new Error('Error en la búsqueda')
      const data = await resp.json()
      setResults(data)
      setActiveTab('listings')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.app}>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg) } }
        input::placeholder { color: rgba(255,255,255,0.35) }
        a:hover { opacity: 0.85 }
        .card:hover { transform: translateY(-2px) }
      `}</style>

      <header style={styles.header}>
        <h1 style={styles.logo}>CAR FINDER GLOBAL</h1>
        <p style={styles.subtitle}>Buscá cualquier auto en el mundo &mdash; specs, listings y precios</p>
      </header>

      <div style={styles.searchBox}>
        <form onSubmit={handleSearch}>
          <div style={styles.inputRow}>
            <input
              style={styles.input}
              placeholder="Marca (ej: BMW)"
              value={make}
              onChange={e => setMake(e.target.value)}
              required
            />
            <input
              style={styles.input}
              placeholder="Modelo (ej: 220i)"
              value={model}
              onChange={e => setModel(e.target.value)}
              required
            />
            <input
              style={styles.input}
              placeholder="Año (opcional)"
              value={year}
              onChange={e => setYear(e.target.value)}
              type="number"
              min="1900"
              max="2027"
            />
            <button
              style={{...styles.button, ...(loading ? styles.buttonDisabled : {})}}
              disabled={loading}
              type="submit"
            >
              {loading ? 'Buscando...' : 'Buscar'}
            </button>
          </div>
        </form>
      </div>

      {loading && (
        <div style={styles.loader}>
          <div style={styles.spinner} />
          <p style={{ color: '#8892b0' }}>Buscando en {'>'}20 fuentes alrededor del mundo...</p>
        </div>
      )}

      {error && (
        <div style={{...styles.searchBox, marginTop: '20px', borderColor: '#ff6b6b'}}>
          <p style={{ color: '#ff6b6b', textAlign: 'center', margin: 0 }}>Error: {error}</p>
        </div>
      )}

      {results && (
        <>
          <div style={styles.statsRow}>
            <div style={styles.stat}>
              <div style={styles.statNumber}>{results.total_listings}</div>
              <div style={styles.statLabel}>Listings encontrados</div>
            </div>
            <div style={styles.stat}>
              <div style={styles.statNumber}>{results.specs?.length || 0}</div>
              <div style={styles.statLabel}>Versiones/Trims</div>
            </div>
            <div style={styles.stat}>
              <div style={styles.statNumber}>{results.sources_searched?.length || 0}</div>
              <div style={styles.statLabel}>Fuentes consultadas</div>
            </div>
            <div style={styles.stat}>
              <div style={styles.statNumber}>{results.price_comparison?.length || 0}</div>
              <div style={styles.statLabel}>Países con precio</div>
            </div>
          </div>

          <div style={styles.tabs}>
            {[
              { key: 'listings', label: `Listings (${results.listings?.length || 0})` },
              { key: 'specs', label: `Specs Técnicas (${results.specs?.length || 0})` },
              { key: 'prices', label: `Comparar Precios (${results.price_comparison?.length || 0})` },
              { key: 'sources', label: 'Fuentes' },
            ].map(tab => (
              <button
                key={tab.key}
                style={{...styles.tab, ...(activeTab === tab.key ? styles.tabActive : {})}}
                onClick={() => setActiveTab(tab.key)}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div style={styles.results}>
            {activeTab === 'listings' && <ListingsTab listings={results.listings || []} />}
            {activeTab === 'specs' && <SpecsTab specs={results.specs || []} />}
            {activeTab === 'prices' && <PricesTab prices={results.price_comparison || []} />}
            {activeTab === 'sources' && <SourcesTab sources={results.sources_searched || []} />}
          </div>
        </>
      )}

      <footer style={styles.footer}>
        <p>Car Finder Global &mdash; BMW Punta del Este</p>
      </footer>
    </div>
  )
}

function ListingsTab({ listings }) {
  if (!listings.length) return <p style={{ textAlign: 'center', color: '#8892b0' }}>No se encontraron listings.</p>

  return listings.map((item, i) => (
    <div key={i} className="card" style={styles.card}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
        <div>
          <h3 style={styles.cardTitle}>
            {countryFlags[item.country_code] || '\uD83C\uDF10'} {item.title}
          </h3>
          <p style={styles.cardMeta}>
            <span style={{...styles.badge, background: 'rgba(0,210,255,0.15)', color: '#00d2ff'}}>
              {item.source}
            </span>
            <span style={{...styles.badge, background: 'rgba(255,255,255,0.08)', color: '#8892b0'}}>
              {item.country}
            </span>
          </p>
        </div>
        {item.price && (
          <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#00d2ff' }}>
            {item.price}
          </div>
        )}
      </div>
      {item.mileage && <p style={styles.cardMeta}>Kilometraje: {item.mileage}</p>}
      <a href={item.url} target="_blank" rel="noopener noreferrer" style={styles.link}>
        Ver en {item.source} &rarr;
      </a>
    </div>
  ))
}

function SpecsTab({ specs }) {
  if (!specs.length) return <p style={{ textAlign: 'center', color: '#8892b0' }}>No se encontraron specs para este modelo.</p>

  return specs.map((spec, i) => (
    <div key={i} style={{...styles.card, marginBottom: '20px'}}>
      <h3 style={styles.cardTitle}>{spec.make} {spec.model} {spec.year} {spec.trim && `- ${spec.trim}`}</h3>
      <div style={styles.specGrid}>
        {spec.engine && <SpecItem label="Motor" value={spec.engine} />}
        {spec.engine_cc && <SpecItem label="Cilindrada" value={`${spec.engine_cc} cc`} />}
        {spec.engine_cylinders && <SpecItem label="Cilindros" value={spec.engine_cylinders} />}
        {spec.horsepower && <SpecItem label="Potencia" value={`${spec.horsepower} HP`} />}
        {spec.torque && <SpecItem label="Torque" value={`${spec.torque} Nm`} />}
        {spec.transmission && <SpecItem label="Transmisión" value={spec.transmission} />}
        {spec.drive_type && <SpecItem label="Tracción" value={spec.drive_type} />}
        {spec.fuel_type && <SpecItem label="Combustible" value={spec.fuel_type} />}
        {spec.body_type && <SpecItem label="Carrocería" value={spec.body_type} />}
        {spec.doors && <SpecItem label="Puertas" value={spec.doors} />}
        {spec.seats && <SpecItem label="Asientos" value={spec.seats} />}
        {spec.weight_kg && <SpecItem label="Peso" value={`${spec.weight_kg} kg`} />}
        {spec.top_speed_kph && <SpecItem label="Vel. Máxima" value={`${spec.top_speed_kph} km/h`} />}
        {spec.acceleration_0_100 && <SpecItem label="0-100 km/h" value={`${spec.acceleration_0_100} seg`} />}
      </div>
    </div>
  ))
}

function SpecItem({ label, value }) {
  return (
    <div style={styles.specItem}>
      <div style={styles.specLabel}>{label}</div>
      <div style={styles.specValue}>{value}</div>
    </div>
  )
}

function PricesTab({ prices }) {
  if (!prices.length) return <p style={{ textAlign: 'center', color: '#8892b0' }}>No hay datos de precios disponibles. Los precios se muestran cuando las fuentes devuelven información de precio.</p>

  const maxPrice = Math.max(...prices.map(p => p.avg_price_usd || 0))

  return (
    <div>
      <p style={{ color: '#8892b0', textAlign: 'center', marginBottom: '20px' }}>
        Comparación de precios promedio por país (USD)
      </p>
      {prices.map((item, i) => (
        <div key={i} style={{...styles.card, display: 'flex', alignItems: 'center', gap: '16px'}}>
          <div style={{ minWidth: '140px' }}>
            <span style={{ fontSize: '1.2rem' }}>{countryFlags[item.country_code] || '\uD83C\uDF10'}</span>
            {' '}
            <strong>{item.country}</strong>
            <div style={{ fontSize: '0.8rem', color: '#8892b0' }}>{item.listing_count} listings</div>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{
              ...styles.priceBar,
              width: `${((item.avg_price_usd || 0) / maxPrice) * 100}%`
            }} />
          </div>
          <div style={{ minWidth: '100px', textAlign: 'right', fontWeight: 700, color: '#00d2ff' }}>
            ${(item.avg_price_usd || 0).toLocaleString()}
          </div>
        </div>
      ))}
    </div>
  )
}

function SourcesTab({ sources }) {
  return (
    <div>
      <p style={{ color: '#8892b0', textAlign: 'center' }}>
        Fuentes consultadas en esta búsqueda
      </p>
      <div style={styles.sourcesGrid}>
        {sources.map((source, i) => (
          <div key={i} style={styles.sourceChip}>
            <span style={{ fontSize: '1.2rem' }}>{'\u2713'}</span>
            {source}
          </div>
        ))}
      </div>
      <div style={{...styles.card, marginTop: '30px'}}>
        <h3 style={styles.cardTitle}>Agregar más fuentes</h3>
        <p style={styles.cardMeta}>
          El sistema es extensible. Se pueden agregar nuevas fuentes de listings editando
          <code style={{ background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px', margin: '0 4px' }}>
            backend/services/listing_sources.py
          </code>
          y creando una nueva clase que herede de <code style={{ background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px' }}>ListingSource</code>.
        </p>
      </div>
    </div>
  )
}

export default App
