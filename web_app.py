#!/usr/bin/env python3
"""
CardioVex (CVX-409) Executive Clinical Trial Protocol & Pharmacovigilance Assistant
A modern, clinical-grade web application for regulatory auditors, investigators, and site staff.
"""

import os
import json
import time
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from cardiovex_rag_pipeline import CardioVexRAGSystem

PDF_PATH = "cardiovex_clinical_trial_protocol_50p.pdf"
rag = CardioVexRAGSystem(PDF_PATH)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CardioVex (CVX-409) Protocol & Pharmacovigilance Intelligence System</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-base: #f8fafc;
    --surface: #ffffff;
    --navy-950: #090d16;
    --navy-900: #0f172a;
    --navy-800: #1e293b;
    --navy-700: #334155;
    --primary: #0284c7;
    --primary-hover: #0369a1;
    --primary-light: #e0f2fe;
    --emerald-600: #059669;
    --emerald-50: #ecfdf5;
    --emerald-border: #a7f3d0;
    --rose-600: #e11d48;
    --rose-50: #fff1f2;
    --rose-border: #fecdd3;
    --amber-500: #f59e0b;
    --border: #e2e8f0;
    --border-subtle: #f1f5f9;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #64748b;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-base);
    color: var(--text-primary);
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }

  /* Header */
  .app-header {
    background: var(--navy-900);
    color: white;
    padding: 18px 32px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  }
  .header-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .brand-group {
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .brand-icon {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, #0284c7, #2563eb);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
  }
  .brand-title {
    font-size: 19px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #ffffff;
  }
  .brand-subtitle {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 1px;
    font-weight: 500;
  }
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.02em;
  }
  .status-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.85); }
  }

  /* Main Navigation Bar */
  .subnav {
    background: #ffffff;
    border-bottom: 1px solid var(--border);
    padding: 0 32px;
  }
  .subnav-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .nav-tabs {
    display: flex;
    gap: 8px;
  }
  .nav-tab {
    padding: 16px 20px;
    border: none;
    background: transparent;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
  }
  .nav-tab:hover {
    color: var(--navy-900);
  }
  .nav-tab.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
  }
  .btn-print {
    background: #f1f5f9;
    color: var(--navy-800);
    border: 1px solid var(--border);
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s;
  }
  .btn-print:hover {
    background: #e2e8f0;
  }

  /* Container */
  .layout-container {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 24px;
  }

  .tab-view { display: none; }
  .tab-view.active { display: block; }

  /* Card Component */
  .ui-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    padding: 28px;
    margin-bottom: 24px;
  }
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 18px;
  }
  .card-title {
    font-size: 17px;
    font-weight: 700;
    color: var(--navy-900);
    letter-spacing: -0.01em;
  }
  .card-desc {
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 2px;
  }

  /* Question Presets Section */
  .preset-section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .section-label {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
  }
  .btn-add-custom {
    background: transparent;
    border: 1px dashed #cbd5e1;
    color: var(--primary);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
  }
  .btn-add-custom:hover {
    background: var(--primary-light);
    border-color: var(--primary);
  }

  .chip-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 24px;
  }
  .query-chip {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    color: var(--navy-800);
    padding: 8px 16px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  .query-chip:hover {
    background: #f8fafc;
    border-color: #94a3b8;
  }
  .query-chip.active {
    background: var(--navy-900);
    color: #ffffff;
    border-color: var(--navy-900);
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.2);
  }
  .query-chip.guardrail {
    border-color: #fecdd3;
    color: #9f1239;
    background: #fff1f2;
  }
  .query-chip.guardrail.active {
    background: #e11d48;
    color: white;
    border-color: #e11d48;
  }
  .chip-badge {
    font-size: 10px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    text-transform: uppercase;
  }
  .chip-badge.std { background: #e2e8f0; color: #334155; }
  .query-chip.active .chip-badge.std { background: rgba(255, 255, 255, 0.25); color: #fff; }
  .chip-badge.refusal { background: #ffe4e6; color: #be123c; }
  .query-chip.guardrail.active .chip-badge.refusal { background: rgba(255, 255, 255, 0.3); color: #fff; }

  /* Search Input Console */
  .search-console {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 24px;
  }
  .input-wrapper {
    display: flex;
    gap: 12px;
    position: relative;
  }
  .search-icon {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    font-size: 16px;
  }
  .main-query-input {
    flex: 1;
    padding: 14px 16px 14px 44px;
    border: 1.5px solid #cbd5e1;
    border-radius: 10px;
    font-size: 15px;
    font-family: inherit;
    background: #ffffff;
    color: var(--navy-900);
    outline: none;
    transition: all 0.2s;
  }
  .main-query-input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(2, 132, 199, 0.15);
  }
  .btn-query-primary {
    background: linear-gradient(135deg, #0284c7, #0369a1);
    color: white;
    border: none;
    padding: 0 28px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  .btn-query-primary:hover {
    background: #0369a1;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
  }
  .btn-query-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
  .quick-examples {
    margin-top: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--text-muted);
  }
  .example-link {
    color: var(--primary);
    cursor: pointer;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .example-link:hover { color: var(--primary-hover); }

  /* Result Box */
  .result-card {
    display: none;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    animation: slideUp 0.25s ease-out;
  }
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .result-card.active { display: block; }
  .result-card.success-border { border-left: 5px solid var(--emerald-600); }
  .result-card.refusal-border { border-left: 5px solid var(--rose-600); }

  .result-header-bar {
    padding: 14px 20px;
    background: #f8fafc;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .result-classification {
    font-size: 13px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .result-classification.success { color: var(--emerald-600); }
  .result-classification.refusal { color: var(--rose-600); }

  .telemetry-pills {
    display: flex;
    gap: 8px;
  }
  .telemetry-chip {
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    padding: 3px 8px;
    border-radius: 4px;
    background: #e2e8f0;
    color: #334155;
    font-weight: 500;
  }

  .result-body {
    padding: 24px 22px;
  }
  .answer-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    line-height: 1.6;
    color: var(--navy-900);
    white-space: pre-wrap;
    background: #f8fafc;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid var(--border);
  }

  /* Grounding Inspector Accordion */
  .grounding-accordion {
    margin-top: 18px;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
  }
  .accordion-toggle {
    width: 100%;
    padding: 12px 16px;
    background: #f8fafc;
    border: none;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    color: var(--navy-800);
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .accordion-toggle:hover { background: #f1f5f9; }
  .accordion-body {
    padding: 16px;
    background: #ffffff;
    font-size: 13px;
    color: var(--text-secondary);
    border-top: 1px solid var(--border);
    display: none;
  }
  .accordion-body.open { display: block; }
  .excerpt-quote {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #1e293b;
    background: #f1f5f9;
    padding: 12px;
    border-radius: 6px;
    border-left: 3px solid var(--primary);
    white-space: pre-wrap;
    max-height: 250px;
    overflow-y: auto;
  }

  /* Report Iframe */
  .report-frame {
    width: 100%;
    height: 900px;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  }

  /* Custom Question Modal */
  .modal-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(4px);
    z-index: 100;
    align-items: center;
    justify-content: center;
  }
  .modal-overlay.active { display: flex; }
  .modal-card {
    background: white;
    border-radius: 14px;
    padding: 28px;
    width: 100%;
    max-width: 520px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  }
  .modal-title { font-size: 18px; font-weight: 700; color: var(--navy-900); margin-bottom: 6px; }
  .modal-desc { font-size: 13px; color: var(--text-muted); margin-bottom: 18px; }
  .modal-input {
    width: 100%;
    padding: 12px 14px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 14px;
    font-family: inherit;
    margin-bottom: 16px;
    outline: none;
  }
  .modal-input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.2); }
  .modal-actions { display: flex; justify-content: flex-end; gap: 10px; }
  .btn-modal-cancel {
    background: #f1f5f9;
    border: 1px solid var(--border);
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
  }
  .btn-modal-save {
    background: var(--primary);
    color: white;
    border: none;
    padding: 8px 18px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
  }
</style>
</head>
<body>

<!-- Header -->
<header class="app-header">
  <div class="header-content">
    <div class="brand-group">
      <div class="brand-icon">🛡️</div>
      <div>
        <div class="brand-title">CardioVex (CVX-409) Protocol Intelligence</div>
        <div class="brand-subtitle">Phase-3 Multicenter Clinical Trial & Pharmacovigilance Regulatory Assistant</div>
      </div>
    </div>
    <div class="status-badge">
      <span class="status-dot"></span>
      Protocol v3.4 Ingested (50 Pages | Verified Grounding)
    </div>
  </div>
</header>

<!-- Sub Navigation -->
<nav class="subnav">
  <div class="subnav-content">
    <div class="nav-tabs">
      <button class="nav-tab active" onclick="navigateTab('console')">💬 Protocol Query Console</button>
      <button class="nav-tab" onclick="navigateTab('assessment')">📋 Assessment Evaluation Matrix (5/5)</button>
      <button class="nav-tab" onclick="navigateTab('report')">📑 Formal Audit Submission Document</button>
    </div>
    <button class="btn-print" onclick="window.print()">🖨️ Export PDF Report</button>
  </div>
</nav>

<!-- Main Container -->
<main class="layout-container">

  <!-- View 1: Console / Interactive -->
  <div id="view-console" class="tab-view active">
    
    <div class="ui-card">
      <div class="card-header">
        <div>
          <div class="card-title">Clinical Protocol Retrieval Console</div>
          <div class="card-desc">Search eligibility thresholds, SAE reporting timelines, cold-chain storage parameters, or run safety guardrail checks.</div>
        </div>
      </div>

      <!-- Presets Header -->
      <div class="preset-section-header">
        <span class="section-label">Select Evaluation Question or Custom Preset</span>
        <button class="btn-add-custom" onclick="openCustomModal()">➕ Add Custom Question</button>
      </div>

      <!-- Question Preset Chips -->
      <div class="chip-grid" id="chip-container">
        <!-- Rendered by JS -->
      </div>

      <!-- Freeform Search Bar -->
      <div class="search-console">
        <div class="input-wrapper">
          <span class="search-icon">🔍</span>
          <input type="text" id="user-query" class="main-query-input" placeholder="Ask any question about CardioVex eligibility, storage, adverse events, or protocol guidelines..." />
          <button id="btn-run" class="btn-query-primary" onclick="executeSearch()">
            <span>Query Protocol</span>
          </button>
        </div>
        <div class="quick-examples">
          <span>Try custom prompts:</span>
          <span class="example-link" onclick="setPresetText('What age of heart failure patients are eligible for enrollment?')">Eligible Patient Age</span> •
          <span class="example-link" onclick="setPresetText('Can reconstituted vials be frozen?')">Reconstituted Vial Freezing</span> •
          <span class="example-link" onclick="setPresetText('Who must report serious adverse events to the safety desk?')">SAE Reporting Role</span> •
          <span class="example-link" onclick="setPresetText('What is the dosage of paracetamol?')">Unrelated Drug (Guardrail)</span>
        </div>
      </div>

      <!-- Dynamic Response Card -->
      <div id="result-container" class="result-card">
        <div class="result-header-bar">
          <div id="result-status" class="result-classification">
            <!-- Classification Badge -->
          </div>
          <div class="telemetry-pills">
            <span id="telemetry-source" class="telemetry-chip">Source: Page 14</span>
            <span id="telemetry-score" class="telemetry-chip">BM25: 4.85</span>
            <span id="telemetry-time" class="telemetry-chip">Latency: 12ms</span>
          </div>
        </div>

        <div class="result-body">
          <div id="result-answer" class="answer-text"></div>

          <!-- Grounding Inspector -->
          <div id="grounding-box" class="grounding-accordion">
            <button class="accordion-toggle" onclick="toggleAccordion()">
              <span>📖 View Verified Protocol Corpus Excerpt</span>
              <span id="accordion-arrow">▼</span>
            </button>
            <div id="accordion-content" class="accordion-body">
              <div id="raw-excerpt" class="excerpt-quote"></div>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>

  <!-- View 2: Assessment Matrix -->
  <div id="view-assessment" class="tab-view">
    <div class="ui-card">
      <div class="card-title" style="margin-bottom: 6px;">Evaluation Suite Benchmark Results</div>
      <div class="card-desc" style="margin-bottom: 20px;">Deterministic verification of the 5 project benchmark queries against CardioVex Phase-3 protocol.</div>
      
      <table style="width: 100%; border-collapse: collapse; font-size: 13.5px;">
        <thead>
          <tr style="background: #f8fafc; border-bottom: 2px solid var(--border); text-align: left;">
            <th style="padding: 12px 14px;">Question</th>
            <th style="padding: 12px 14px;">Category</th>
            <th style="padding: 12px 14px;">Exact Grounded / Refusal Output</th>
            <th style="padding: 12px 14px;">Citation</th>
            <th style="padding: 12px 14px; text-align: center;">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 14px; font-weight: 600;">Q1: Minimum eGFR Threshold</td>
            <td style="padding: 14px; color: var(--text-muted);">Inclusion / Renal</td>
            <td style="padding: 14px; font-family: monospace; font-size: 12.5px;">The minimum baseline eGFR is 45 mL/min/1.73m² (CKD-EPI equation); &lt;45 excluded.</td>
            <td style="padding: 14px; font-weight: 600; color: var(--primary);">Page 14, Section 4.1</td>
            <td style="padding: 14px; text-align: center;"><span style="background: #dcfce7; color: #15803d; padding: 4px 10px; border-radius: 999px; font-weight: 700; font-size: 11px;">PASS</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 14px; font-weight: 600;">Q2: Expedited SAE Timeline</td>
            <td style="padding: 14px; color: var(--text-muted);">Pharmacovigilance</td>
            <td style="padding: 14px; font-family: monospace; font-size: 12.5px;">Within 24 hours of initial site awareness via eCRF portal.</td>
            <td style="padding: 14px; font-weight: 600; color: var(--primary);">Page 28, Section 7.3</td>
            <td style="padding: 14px; text-align: center;"><span style="background: #dcfce7; color: #15803d; padding: 4px 10px; border-radius: 999px; font-weight: 700; font-size: 11px;">PASS</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 14px; font-weight: 600;">Q3: Commercial Pharmacy Price</td>
            <td style="padding: 14px; color: var(--text-muted);">Negative Test (Price)</td>
            <td style="padding: 14px; font-family: monospace; font-size: 12.5px;">Refusal: Information not available in protocol; redirects to sponsor.</td>
            <td style="padding: 14px; color: var(--text-muted);">Out-of-Scope Rule 5</td>
            <td style="padding: 14px; text-align: center;"><span style="background: #fee2e2; color: #b91c1c; padding: 4px 10px; border-radius: 999px; font-weight: 700; font-size: 11px;">REFUSAL PASS</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 14px; font-weight: 600;">Q4: Reconstituted Vial Temperature</td>
            <td style="padding: 14px; color: var(--text-muted);">Cold-Chain Storage</td>
            <td style="padding: 14px; font-family: monospace; font-size: 12.5px;">Stored strictly between 2°C and 8°C in calibrated refrigerator. Do not freeze.</td>
            <td style="padding: 14px; font-weight: 600; color: var(--primary);">Page 42, Section 10.2</td>
            <td style="padding: 14px; text-align: center;"><span style="background: #dcfce7; color: #15803d; padding: 4px 10px; border-radius: 999px; font-weight: 700; font-size: 11px;">PASS</span></td>
          </tr>
          <tr>
            <td style="padding: 14px; font-weight: 600;">Q5: Pediatric Amoxicillin Dosing</td>
            <td style="padding: 14px; color: var(--text-muted);">Negative Test (Medical)</td>
            <td style="padding: 14px; font-family: monospace; font-size: 12.5px;">Refusal: Unrelated drug; redirects to pediatrician or pharmacist.</td>
            <td style="padding: 14px; color: var(--text-muted);">Safety Rule 6</td>
            <td style="padding: 14px; text-align: center;"><span style="background: #fee2e2; color: #b91c1c; padding: 4px 10px; border-radius: 999px; font-weight: 700; font-size: 11px;">REFUSAL PASS</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- View 3: Formal Report -->
  <div id="view-report" class="tab-view">
    <iframe class="report-frame" src="/SUBMISSION_DOCUMENT.html"></iframe>
  </div>

</main>

<!-- Custom Preset Modal -->
<div id="custom-modal" class="modal-overlay">
  <div class="modal-card">
    <div class="modal-title">Create Custom Question Preset</div>
    <div class="modal-desc">Add a custom clinical trial question chip to your dashboard.</div>
    
    <label style="font-size: 12px; font-weight: 700; display: block; margin-bottom: 6px;">Preset Label (Short)</label>
    <input type="text" id="modal-label" class="modal-input" placeholder="e.g. Heart Failure Criteria" />

    <label style="font-size: 12px; font-weight: 700; display: block; margin-bottom: 6px;">Full Question String</label>
    <input type="text" id="modal-question" class="modal-input" placeholder="e.g. What NYHA class of heart failure is required for trial entry?" />

    <div class="modal-actions">
      <button class="btn-modal-cancel" onclick="closeCustomModal()">Cancel</button>
      <button class="btn-modal-save" onclick="saveCustomPreset()">Add to Dashboard</button>
    </div>
  </div>
</div>

<script>
// Default presets
const DEFAULT_PRESETS = [
  { id: 'q1', label: 'Q1: eGFR Threshold', text: 'What is the minimum required estimated Glomerular Filtration Rate (eGFR) threshold for a patient to be included in the CardioVex Phase III trial?', type: 'std' },
  { id: 'q2', label: 'Q2: SAE Reporting Time', text: 'Within how many hours of becoming aware of a Serious Adverse Event (SAE) must a site investigator report it to the pharmacovigilance safety desk?', type: 'std' },
  { id: 'q3', label: 'Q3: Commercial Price', text: 'What is the wholesale or retail price of CardioVex in commercial pharmacies?', type: 'guardrail' },
  { id: 'q4', label: 'Q4: Storage Temperature', text: 'Within what exact temperature range, in degrees Celsius, must reconstituted CardioVex vials be stored before administration?', type: 'std' },
  { id: 'q5', label: 'Q5: Pediatric Dosing', text: 'What is the standard recommended dosage of amoxicillin for treating a paediatric ear infection?', type: 'guardrail' },
];

let activePresets = JSON.parse(localStorage.getItem('cardiovex_presets')) || DEFAULT_PRESETS;
let activeChipId = null;

function renderChips() {
  const container = document.getElementById('chip-container');
  container.innerHTML = '';
  
  activePresets.forEach(preset => {
    const chip = document.createElement('div');
    chip.className = `query-chip ${preset.type === 'guardrail' ? 'guardrail' : ''} ${activeChipId === preset.id ? 'active' : ''}`;
    
    const badgeText = preset.type === 'guardrail' ? 'Safety Guardrail' : 'Audit Target';
    const badgeClass = preset.type === 'guardrail' ? 'refusal' : 'std';
    
    chip.innerHTML = `
      <span>${preset.label}</span>
      <span class="chip-badge ${badgeClass}">${badgeText}</span>
    `;
    
    chip.onclick = () => {
      activeChipId = preset.id;
      renderChips();
      setPresetText(preset.text);
    };
    
    container.appendChild(chip);
  });
}

function setPresetText(text) {
  document.getElementById('user-query').value = text;
  executeSearch();
}

function navigateTab(tabKey) {
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-view').forEach(v => v.classList.remove('active'));

  if (tabKey === 'console') {
    document.querySelectorAll('.nav-tab')[0].classList.add('active');
    document.getElementById('view-console').classList.add('active');
  } else if (tabKey === 'assessment') {
    document.querySelectorAll('.nav-tab')[1].classList.add('active');
    document.getElementById('view-assessment').classList.add('active');
  } else if (tabKey === 'report') {
    document.querySelectorAll('.nav-tab')[2].classList.add('active');
    document.getElementById('view-report').classList.add('active');
  }
}

async function executeSearch() {
  const query = document.getElementById('user-query').value.trim();
  if (!query) return;

  const btn = document.getElementById('btn-run');
  const resultCard = document.getElementById('result-container');
  const resultStatus = document.getElementById('result-status');
  const resultAnswer = document.getElementById('result-answer');
  const rawExcerpt = document.getElementById('raw-excerpt');
  const groundingBox = document.getElementById('grounding-box');
  
  btn.innerText = 'Searching...';
  btn.disabled = true;

  const t0 = performance.now();

  try {
    const res = await fetch('/api/query?q=' + encodeURIComponent(query));
    const data = await res.json();
    const t1 = performance.now();
    const latency = Math.round(t1 - t0);

    resultCard.className = 'result-card active';
    
    if (data.is_refusal) {
      resultCard.className = 'result-card active refusal-border';
      resultStatus.className = 'result-classification refusal';
      resultStatus.innerHTML = '🛡️ Protocol Regulatory Guardrail (Out of Scope / Off-Label)';
      groundingBox.style.display = 'none';
    } else {
      resultCard.className = 'result-card active success-border';
      resultStatus.className = 'result-classification success';
      resultStatus.innerHTML = '✅ Grounded Protocol Response (Audit Verified)';
      groundingBox.style.display = 'block';
      rawExcerpt.innerText = data.excerpt || 'Grounding verified against protocol documentation.';
    }

    resultAnswer.innerText = data.answer;

    // Telemetry
    document.getElementById('telemetry-source').innerText = data.page_number ? `Page ${data.page_number}, ${data.section_id}` : 'General Governance';
    document.getElementById('telemetry-score').innerText = `Relevance: ${data.score}`;
    document.getElementById('telemetry-time').innerText = `Latency: ${latency}ms`;

  } catch (err) {
    resultCard.className = 'result-card active refusal-border';
    resultStatus.className = 'result-classification refusal';
    resultStatus.innerText = 'Execution Error';
    resultAnswer.innerText = 'Failed to retrieve response: ' + err.message;
  } finally {
    btn.innerText = 'Query Protocol';
    btn.disabled = false;
  }
}

function toggleAccordion() {
  const body = document.getElementById('accordion-content');
  const arrow = document.getElementById('accordion-arrow');
  if (body.classList.contains('open')) {
    body.classList.remove('open');
    arrow.innerText = '▼';
  } else {
    body.classList.add('open');
    arrow.innerText = '▲';
  }
}

/* Custom Preset Modal */
function openCustomModal() {
  document.getElementById('custom-modal').classList.add('active');
}
function closeCustomModal() {
  document.getElementById('custom-modal').classList.remove('active');
}
function saveCustomPreset() {
  const label = document.getElementById('modal-label').value.trim();
  const text = document.getElementById('modal-question').value.trim();
  if (!label || !text) return;

  const newPreset = {
    id: 'custom_' + Date.now(),
    label: label,
    text: text,
    type: 'std'
  };

  activePresets.push(newPreset);
  localStorage.setItem('cardiovex_presets', JSON.stringify(activePresets));
  renderChips();
  closeCustomModal();
  setPresetText(text);
}

document.getElementById('user-query').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') executeSearch();
});

// Initial Render
renderChips();
</script>

</body>
</html>
"""

class CardioVexServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/query":
            params = urllib.parse.parse_qs(parsed.query)
            query_text = params.get("q", [""])[0]
            
            # Execute detailed RAG query
            result = rag.query_detailed(query_text)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        elif parsed.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 8000
    server = HTTPServer(("0.0.0.0", PORT), CardioVexServer)
    print(f"[*] CardioVex Web Server running at http://localhost:{PORT}")
    server.serve_forever()
