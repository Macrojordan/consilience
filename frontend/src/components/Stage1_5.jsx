import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './Stage1_5.css';

export default function Stage1_5({ critiques }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!critiques || critiques.length === 0) {
    return null;
  }

  return (
    <div className="stage stage1_5">
      <h3 className="stage-title">Stage 1.5: Cross-Examination</h3>
      <p className="stage-description">
        Each model critically examines all responses, identifying errors, flaws, and missing information.
      </p>

      <div className="tabs">
        {critiques.map((critique, index) => (
          <button
            key={index}
            className={`tab ${activeTab === index ? 'active' : ''}`}
            onClick={() => setActiveTab(index)}
          >
            {critique.model.split('/')[1] || critique.model}
          </button>
        ))}
      </div>

      <div className="tab-content">
        <div className="model-name">{critiques[activeTab].model}</div>
        <div className="critique-text markdown-content">
          <ReactMarkdown>{critiques[activeTab].critique}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
