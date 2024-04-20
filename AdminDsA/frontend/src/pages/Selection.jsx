import React, { useState } from 'react';
import './Selection.css';

function Selection() {
  const [serviceLib, setServiceLib] = useState('');
  const [serviceName, setServiceName] = useState('');
  const [vcpu, setVCPU] = useState('');
  const [ram, setRAM] = useState('');
  const [tps, setTPS] = useState('');
  const [showOptions, setShowOptions] = useState(false); // State to manage whether to show additional options
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send form data to the backend
      const response = await fetch('/api/services', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          serviceLib,
          serviceName,
          vcpu,
          ram,
          tps,
          selectedOptions
        })
      });
      // Handle success or show a success message
      const data = await response.json();
      console.log('Form submitted successfully:', data);
    } catch (error) {
      // Handle error or show an error message
      console.error('Error submitting form:', error);
    }
  };

  return (
    <form className="service-form" onSubmit={handleSubmit}>
      <div>
        <label htmlFor="serviceLib">Service Library:</label>
        <select id="serviceLib" value={serviceLib} onChange={(e) => setServiceLib(e.target.value)}>
          <option value="">Select Service Library</option>
          <option value="AUSF">AUSF</option>
          <option value="UDM">UDM</option>
          <option value="EIR">EIR</option>
          <option value="HSS">HSS</option>
          <option value="Support">Supporting Lib</option>
        </select>
      </div>
      <div>
        <label htmlFor="serviceName">Service Name:</label>
        <input type="text" id="serviceName" value={serviceName} onChange={(e) => setServiceName(e.target.value)} />
      </div>
      <div>
        <label htmlFor="additionalOptions">Dependencies:</label>
        <input type="checkbox" id="additionalOptions" checked={showOptions} onChange={(e) => setShowOptions(e.target.checked)} />
        <label htmlFor="additionalOptions">Yes</label>
    </div>
    <div>
        <input type="checkbox" id="noOptions" checked={!showOptions} onChange={(e) => setShowOptions(!e.target.checked)} />
        <label htmlFor="noOptions">No</label>
    </div>
      {showOptions && (
        <div>
          {/* Additional options to select */}
          <label>Select Options:</label>
          <input type="checkbox" id="Ausf_ueAuth" value="Ausf_ueAuth" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Ausf_ueAuth">Ausf_ueAuth</label>
          <input type="checkbox" id="Ausf_niddau" value="Ausf_niddau" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Ausf_niddau">Ausf_niddau</label>
          <input type="checkbox" id="Udm_uecm" value="Udm_uecm" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Udm_uecm">Udm_uecm</label>
          <input type="checkbox" id="Udm_ueauth" value="Udm_ueauth" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Udm_ueauth">Udm_ueauth</label>
          <input type="checkbox" id="Udm_sidf" value="Udm_sidf" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Udm_sidf">Udm_sidf</label>
          <input type="checkbox" id="Udm_sdm" value="Udm_sdm" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Udm_sdm">Udm_sdm</label>
          <input type="checkbox" id="EIR_deviceCheck" value="EIR_deviceCheck" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="EIR_deviceCheck">EIR_deviceCheck</label>
          <input type="checkbox" id="Hss_ims" value="Hss_ims" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Hss_ims">Hss_ims</label>
          <input type="checkbox" id="HSS_lte" value="HSS_lte" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="HSS_lte">HSS_lte</label>
          <input type="checkbox" id="Hss_auth" value="Hss_auth" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Hss_auth">Hss_auth</label>
          <input type="checkbox" id="Hlr_callp" value="Hlr_callp" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Hlr_callp">Hlr_callp</label>
          <input type="checkbox" id="Hlr_auth" value="Hlr_auth" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Hlr_auth">Hlr_auth</label>
          <input type="checkbox" id="HTTPLB" value="HTTPLB" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="HTTPLB">HTTPLB</label>
          <input type="checkbox" id="DiameterLB" value="DiameterLB" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="DiameterLB">DiameterLB</label>
          <input type="checkbox" id="SS7LB" value="SS7LB" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="SS7LB">SS7LB</label>
          <input type="checkbox" id="Reg_trigger" value="Reg_trigger" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Reg_trigger">Reg_trigger</label>
          <input type="checkbox" id="Lawful Interception" value="Lawful Interception" onChange={(e) => handleOptionChange(e.target.value)} />
          <label htmlFor="Lawful Interception">Lawful Interception</label>
        </div>
      )}
      <div>
        <label htmlFor="vcpu">VCPU:</label>
        <input type="number" id="vcpu" value={vcpu} onChange={(e) => setVCPU(e.target.value)} />
      </div>
      <div>
        <label htmlFor="ram">RAM:</label>
        <input type="number" id="ram" value={ram} onChange={(e) => setRAM(e.target.value)} />
      </div>
      <div>
        <label htmlFor="tps">TPS:</label>
        <input type="number" id="tps" value={tps} onChange={(e) => setTPS(e.target.value)} />
      </div>
      <button type="submit">Submit</button>
    </form>
  );

  function handleOptionChange(option) {
    const currentIndex = selectedOptions.indexOf(option);
    const newSelectedOptions = [...selectedOptions];

    if (currentIndex === -1) {
      newSelectedOptions.push(option);
    } else {
      newSelectedOptions.splice(currentIndex, 1);
    }

    setSelectedOptions(newSelectedOptions);
  }
}

export default Selection;
