import React, { useState } from 'react';
import { NextUIProvider } from '@nextui-org/react';
import {
  Card,
  CardBody,
  CardHeader,
  Button,
  Chip,
  Progress,
  Divider,
  Alert,
  Select,
  SelectItem
} from '@nextui-org/react';
import {
  BarChart3,
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  Activity,
  Calendar,
  Target,
  Lightbulb,
  CheckCircle,
  XCircle
} from 'lucide-react';
import axios from 'axios';
import Header from './components/Header';
import AnalysisResults from './components/AnalysisResults';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState('unknown');
  const [availableAssets, setAvailableAssets] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState('USD INDEX');

  // Check backend health and load assets on component mount
  React.useEffect(() => {
    const initializeApp = async () => {
      try {
        // Check backend health
        const healthResponse = await axios.get('http://localhost:5000/api/health', {
          timeout: 5000
        });
        if (healthResponse.data.status === 'healthy') {
          setBackendStatus('healthy');

          // Load available assets
          const assetsResponse = await axios.get('http://localhost:5000/api/assets', {
            timeout: 5000
          });
          const assets = assetsResponse.data.assets || [];
          setAvailableAssets(assets);

          // Set default asset if not already set and assets are available
          if (assets.length > 0 && !selectedAsset) {
            setSelectedAsset(assets[0].name);
          }
        }
      } catch (err) {
        setBackendStatus('unhealthy');
        console.warn('Backend initialization failed:', err.message);
      }
    };

    initializeApp();
  }, []);

  const runAnalysis = async () => {
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      // Use absolute URL to avoid proxy issues
      const response = await axios.post('http://localhost:5000/api/analyze', {
        asset: selectedAsset
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000, // 30 second timeout
      });
      setAnalysis(response.data);
    } catch (err) {
      console.error('Analysis error:', err);
      if (err.code === 'ECONNREFUSED' || err.message.includes('Network Error')) {
        setError('Cannot connect to the backend server. Please make sure the backend is running on http://localhost:5000');
      } else {
        setError(err.response?.data?.error || 'Failed to run analysis. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };



  return (
    <NextUIProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-200 p-4 md:p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Header Section */}
          <Card className="shadow-lg border-0">
            <CardHeader className="pb-4">
              <div className="flex flex-col items-center text-center w-full">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 bg-primary-100 rounded-full">
                    <Activity className="w-8 h-8 text-primary-600" />
                  </div>
                  <h1 className="text-3xl md:text-4xl font-bold text-slate-800">
                    USD Index COT Analyzer
                  </h1>
                </div>
                <p className="text-slate-600 text-lg max-w-3xl leading-relaxed">
                  Analyze CFTC Commitments of Traders data for the USD Index to identify
                  directional bias and trading opportunities based on institutional positioning.
                </p>
              </div>
            </CardHeader>
          </Card>

          {/* Status and Control Section */}
          <Card className="shadow-lg border-0">
            <CardBody className="p-6">
              <div className="flex flex-col items-center space-y-6">
                {/* Backend Status */}
                <div className="flex items-center gap-2">
                  {backendStatus === 'healthy' ? (
                    <Chip
                      startContent={<CheckCircle size={16} />}
                      color="success"
                      variant="flat"
                      size="sm"
                    >
                      Backend Connected ({availableAssets.length} assets available)
                    </Chip>
                  ) : backendStatus === 'unhealthy' ? (
                    <Chip
                      startContent={<XCircle size={16} />}
                      color="danger"
                      variant="flat"
                      size="sm"
                    >
                      Backend Disconnected
                    </Chip>
                  ) : (
                    <Chip
                      startContent={<Activity size={16} />}
                      color="warning"
                      variant="flat"
                      size="sm"
                    >
                      Checking Connection...
                    </Chip>
                  )}
                </div>

                {/* Asset Selection */}
                {backendStatus === 'healthy' && (
                  <div className="w-full max-w-md">
                    {availableAssets.length > 0 ? (
                      <>
                        <Select
                          label="Select Asset to Analyze"
                          placeholder="Choose an asset"
                          selectedKeys={selectedAsset ? new Set([selectedAsset]) : new Set()}
                          onSelectionChange={(keys) => {
                            const selected = Array.from(keys)[0];
                            if (selected) {
                              setSelectedAsset(selected);
                              setAnalysis(null); // Clear previous analysis when asset changes
                            }
                          }}
                          className="w-full"
                          variant="bordered"
                          size="lg"
                        >
                          {availableAssets.map((asset) => (
                            <SelectItem key={asset.name} value={asset.name}>
                              {asset.name}
                            </SelectItem>
                          ))}
                        </Select>

                        {/* Asset Description */}
                        {selectedAsset && (
                          <div className="mt-2 text-center">
                            <p className="text-sm text-slate-600">
                              {availableAssets.find(a => a.name === selectedAsset)?.description}
                            </p>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="text-center">
                        <p className="text-slate-600">Loading available assets...</p>
                        <Progress size="sm" isIndeterminate className="mt-2" />
                      </div>
                    )}
                  </div>
                )}

                {/* Error Alert */}
                {backendStatus === 'unhealthy' && (
                  <Alert
                    color="danger"
                    variant="flat"
                    startContent={<AlertTriangle size={20} />}
                    className="max-w-2xl"
                  >
                    Backend server is not responding. Please make sure it's running on http://localhost:5000
                  </Alert>
                )}

                {/* Main Action Button */}
                <Button
                  size="lg"
                  color="primary"
                  variant="shadow"
                  startContent={loading ? null : <BarChart3 size={20} />}
                  onClick={runAnalysis}
                  disabled={loading || backendStatus === 'unhealthy' || !selectedAsset}
                  className="px-8 py-6 text-lg font-semibold"
                >
                  {loading ? (
                    <div className="flex items-center gap-3">
                      <div className="loading-spinner" />
                      Analyzing {selectedAsset}...
                    </div>
                  ) : (
                    `Analyze ${selectedAsset}`
                  )}
                </Button>

                {/* Loading Progress */}
                {loading && (
                  <div className="w-full max-w-md">
                    <Progress
                      size="sm"
                      isIndeterminate
                      color="primary"
                      className="max-w-md"
                    />
                    <p className="text-sm text-slate-600 text-center mt-2">
                      Fetching latest CFTC data and running analysis...
                    </p>
                  </div>
                )}
              </div>
            </CardBody>
          </Card>

          {/* Error Display */}
          {error && (
            <Alert
              color="danger"
              variant="flat"
              startContent={<AlertTriangle size={20} />}
            >
              {error}
            </Alert>
          )}

          {/* Analysis Results */}
          {analysis && <AnalysisResults analysis={analysis} />}
        </div>
      </div>
    </NextUIProvider>
  );
}

export default App;
