import React, { useRef, useState } from 'react'

export default function UploadArea({ onFileSelected }) {
  const inputRef = useRef(null)
  const [fileName, setFileName] = useState(null)
  const [dragOver, setDragOver] = useState(false)

  function handleClick() {
    inputRef.current.click()
  }

  function handleFile(e) {
    const f = e.target.files?.[0]
    if (f) {
      setFileName(f.name)
      onFileSelected(f)
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files?.[0]
    if (f && f.type === 'application/pdf') {
      setFileName(f.name)
      onFileSelected(f)
    } else {
      alert('Por favor, envie um arquivo PDF.')
    }
  }

  return (
    <div>
      <div
        className={`dropzone ${dragOver ? 'dragover' : ''}`}
        onClick={handleClick}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          style={{ display: 'none' }}
          onChange={handleFile}
        />
        <div className="drop-content">
          <div className="icon">📄</div>
          <div>
            <p className="drop-text">Arraste e solte o edital (PDF) aqui</p>
            <p className="muted">ou clique para selecionar — {fileName ?? 'nenhum arquivo selecionado'}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
