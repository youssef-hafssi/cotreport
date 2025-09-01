import React from 'react';
import {
  Card,
  CardBody,
  CardHeader,
  Chip,
  Divider,
  Progress,
  Alert,
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell
} from '@nextui-org/react';
import {
  TrendingUp,
  TrendingDown,
  Minus,
  BarChart3,
  AlertTriangle,
  Target,
  Lightbulb,
  Calendar,
  DollarSign,
  Activity,
  ArrowUp,
  ArrowDown,
  BookOpen,
  Clock,
  Zap
} from 'lucide-react';



const AnalysisResults = ({ analysis }) => {
  const getBiasIcon = (bias) => {
    if (bias.includes('BULLISH')) return <TrendingUp size={24} />;
    if (bias.includes('BEARISH')) return <TrendingDown size={24} />;
    return <Minus size={24} />;
  };

  const getBiasColor = (bias) => {
    if (bias.includes('BULLISH')) return 'success';
    if (bias.includes('BEARISH')) return 'danger';
    return 'warning';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence === 'HIGH') return 'success';
    if (confidence === 'MEDIUM') return 'warning';
    return 'default';
  };

  const getSignalColor = (signal) => {
    if (signal.includes('BULLISH')) return 'success';
    if (signal.includes('BEARISH')) return 'danger';
    return 'primary';
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat().format(num);
  };

  const formatPercentage = (num) => {
    return `${num?.toFixed(1)}%`;
  };

  return (
    <div className="space-y-6">
      {/* Overall Bias Card */}
      <Card className="shadow-lg border-0">
        <CardBody className="p-6">
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="flex items-center gap-3">
              <div className={`p-3 rounded-full ${
                analysis.analysis.overall_bias.includes('BULLISH')
                  ? 'bg-success-100 text-success-600'
                  : analysis.analysis.overall_bias.includes('BEARISH')
                  ? 'bg-danger-100 text-danger-600'
                  : 'bg-warning-100 text-warning-600'
              }`}>
                {getBiasIcon(analysis.analysis.overall_bias)}
              </div>
              <h2 className="text-2xl md:text-3xl font-bold text-slate-800">
                {analysis.analysis.overall_bias}
              </h2>
            </div>

            <div className="flex items-center gap-4">
              <Chip
                color={getConfidenceColor(analysis.analysis.confidence)}
                variant="flat"
                size="lg"
                className="font-semibold"
              >
                {analysis.analysis.confidence} Confidence
              </Chip>

              <div className="flex items-center gap-2 text-slate-600">
                <Calendar size={16} />
                <span className="text-sm">Report Date: {analysis.data.report_date}</span>
              </div>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Key Metrics */}
      <Card className="shadow-lg border-0">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary-600" />
            <h3 className="text-xl font-semibold text-slate-800">Key Metrics</h3>
          </div>
        </CardHeader>
        <CardBody className="pt-0">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Total Open Interest */}
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600 font-medium">Total Open Interest</span>
                <DollarSign className="w-4 h-4 text-slate-500" />
              </div>
              <div className="text-2xl font-bold text-slate-800">
                {formatNumber(analysis.data.total_open_interest)}
              </div>
              <div className="text-xs text-slate-500 mt-1">contracts</div>
            </div>

            {/* Non-Commercial Net Position */}
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600 font-medium">Non-Commercial Net</span>
                {analysis.metrics.non_commercial_net >= 0 ?
                  <ArrowUp className="w-4 h-4 text-success-500" /> :
                  <ArrowDown className="w-4 h-4 text-danger-500" />
                }
              </div>
              <div className={`text-2xl font-bold ${
                analysis.metrics.non_commercial_net >= 0 ? 'text-success-600' : 'text-danger-600'
              }`}>
                {analysis.metrics.non_commercial_net >= 0 ? '+' : ''}
                {formatNumber(analysis.metrics.non_commercial_net)}
              </div>
              <div className="text-xs text-slate-500 mt-1">contracts</div>
            </div>

            {/* Commercial Net Position */}
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600 font-medium">Commercial Net</span>
                {analysis.metrics.commercial_net >= 0 ?
                  <ArrowUp className="w-4 h-4 text-success-500" /> :
                  <ArrowDown className="w-4 h-4 text-danger-500" />
                }
              </div>
              <div className={`text-2xl font-bold ${
                analysis.metrics.commercial_net >= 0 ? 'text-success-600' : 'text-danger-600'
              }`}>
                {analysis.metrics.commercial_net >= 0 ? '+' : ''}
                {formatNumber(analysis.metrics.commercial_net)}
              </div>
              <div className="text-xs text-slate-500 mt-1">contracts</div>
            </div>

            {/* Speculative Long % */}
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600 font-medium">Speculative Long</span>
                <TrendingUp className="w-4 h-4 text-primary-500" />
              </div>
              <div className="text-2xl font-bold text-slate-800">
                {formatPercentage(analysis.metrics.non_commercial_long_pct)}
              </div>
              <Progress
                value={analysis.metrics.non_commercial_long_pct}
                color="primary"
                size="sm"
                className="mt-2"
              />
            </div>

            {/* Speculative Short % */}
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600 font-medium">Speculative Short</span>
                <TrendingDown className="w-4 h-4 text-danger-500" />
              </div>
              <div className="text-2xl font-bold text-slate-800">
                {formatPercentage(analysis.metrics.non_commercial_short_pct)}
              </div>
              <Progress
                value={analysis.metrics.non_commercial_short_pct}
                color="danger"
                size="sm"
                className="mt-2"
              />
            </div>

            {/* Long/Short Ratio */}
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600 font-medium">Long/Short Ratio</span>
                <BarChart3 className="w-4 h-4 text-slate-500" />
              </div>
              <div className="text-2xl font-bold text-slate-800">
                {analysis.metrics.non_commercial_ratio?.toFixed(2)}
              </div>
              <div className="text-xs text-slate-500 mt-1">
                {analysis.metrics.non_commercial_ratio > 1 ? 'Long bias' : 'Short bias'}
              </div>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Non-Commercial vs Commercial Comparison Table */}
      <Card className="shadow-lg border-0">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-primary-600" />
            <h3 className="text-xl font-semibold text-slate-800">Non-Commercial vs Commercial Comparison</h3>
          </div>
        </CardHeader>
        <CardBody className="pt-0">
          <Table
            aria-label="Non-Commercial vs Commercial comparison"
            className="min-w-full"
            removeWrapper
          >
            <TableHeader>
              <TableColumn className="text-left font-semibold">Position Type</TableColumn>
              <TableColumn className="text-center font-semibold">Non-Commercial (Speculators)</TableColumn>
              <TableColumn className="text-center font-semibold">Commercial (Hedgers)</TableColumn>
              <TableColumn className="text-center font-semibold">Difference</TableColumn>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell className="font-medium">Long Positions</TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <span className="text-lg font-semibold text-slate-800">
                      {formatNumber(analysis.data.non_commercial_long)}
                    </span>
                    <span className="text-xs text-slate-500">
                      {formatPercentage(analysis.metrics.non_commercial_long_pct)}
                    </span>
                  </div>
                </TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <span className="text-lg font-semibold text-slate-800">
                      {formatNumber(analysis.data.commercial_long)}
                    </span>
                    <span className="text-xs text-slate-500">
                      {formatPercentage(analysis.metrics.commercial_long_pct)}
                    </span>
                  </div>
                </TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <span className={`text-lg font-semibold ${
                      (analysis.data.non_commercial_long - analysis.data.commercial_long) >= 0
                        ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {(analysis.data.non_commercial_long - analysis.data.commercial_long) >= 0 ? '+' : ''}
                      {formatNumber(analysis.data.non_commercial_long - analysis.data.commercial_long)}
                    </span>
                    <span className="text-xs text-slate-500">contracts</span>
                  </div>
                </TableCell>
              </TableRow>

              <TableRow>
                <TableCell className="font-medium">Short Positions</TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <span className="text-lg font-semibold text-slate-800">
                      {formatNumber(analysis.data.non_commercial_short)}
                    </span>
                    <span className="text-xs text-slate-500">
                      {formatPercentage(analysis.metrics.non_commercial_short_pct)}
                    </span>
                  </div>
                </TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <span className="text-lg font-semibold text-slate-800">
                      {formatNumber(analysis.data.commercial_short)}
                    </span>
                    <span className="text-xs text-slate-500">
                      {formatPercentage(analysis.metrics.commercial_short_pct)}
                    </span>
                  </div>
                </TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <span className={`text-lg font-semibold ${
                      (analysis.data.non_commercial_short - analysis.data.commercial_short) >= 0
                        ? 'text-danger-600' : 'text-success-600'
                    }`}>
                      {(analysis.data.non_commercial_short - analysis.data.commercial_short) >= 0 ? '+' : ''}
                      {formatNumber(analysis.data.non_commercial_short - analysis.data.commercial_short)}
                    </span>
                    <span className="text-xs text-slate-500">contracts</span>
                  </div>
                </TableCell>
              </TableRow>

              <TableRow className="bg-slate-50">
                <TableCell className="font-semibold">Net Position</TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <Chip
                      color={analysis.metrics.non_commercial_net >= 0 ? 'success' : 'danger'}
                      variant="flat"
                      size="sm"
                      startContent={
                        analysis.metrics.non_commercial_net >= 0 ?
                        <ArrowUp size={14} /> : <ArrowDown size={14} />
                      }
                    >
                      {analysis.metrics.non_commercial_net >= 0 ? '+' : ''}
                      {formatNumber(analysis.metrics.non_commercial_net)}
                    </Chip>
                    <span className="text-xs text-slate-500 mt-1">
                      {analysis.metrics.non_commercial_net >= 0 ? 'Net Long' : 'Net Short'}
                    </span>
                  </div>
                </TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <Chip
                      color={analysis.metrics.commercial_net >= 0 ? 'success' : 'danger'}
                      variant="flat"
                      size="sm"
                      startContent={
                        analysis.metrics.commercial_net >= 0 ?
                        <ArrowUp size={14} /> : <ArrowDown size={14} />
                      }
                    >
                      {analysis.metrics.commercial_net >= 0 ? '+' : ''}
                      {formatNumber(analysis.metrics.commercial_net)}
                    </Chip>
                    <span className="text-xs text-slate-500 mt-1">
                      {analysis.metrics.commercial_net >= 0 ? 'Net Long' : 'Net Short'}
                    </span>
                  </div>
                </TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center">
                    <span className={`text-lg font-bold ${
                      (analysis.metrics.non_commercial_net - analysis.metrics.commercial_net) >= 0
                        ? 'text-primary-600' : 'text-warning-600'
                    }`}>
                      {(analysis.metrics.non_commercial_net - analysis.metrics.commercial_net) >= 0 ? '+' : ''}
                      {formatNumber(analysis.metrics.non_commercial_net - analysis.metrics.commercial_net)}
                    </span>
                    <span className="text-xs text-slate-500">net difference</span>
                  </div>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>

          {/* Table Insights */}
          <div className="mt-4 p-4 bg-slate-50 rounded-lg">
            <h4 className="font-semibold text-slate-700 mb-2 flex items-center gap-2">
              <Target className="w-4 h-4" />
              Key Insights
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                <span className="text-slate-600">
                  <strong>Speculators</strong> are {analysis.metrics.non_commercial_net >= 0 ? 'net long' : 'net short'} by {formatNumber(Math.abs(analysis.metrics.non_commercial_net))} contracts
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-secondary-500 rounded-full"></div>
                <span className="text-slate-600">
                  <strong>Commercials</strong> are {analysis.metrics.commercial_net >= 0 ? 'net long' : 'net short'} by {formatNumber(Math.abs(analysis.metrics.commercial_net))} contracts
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-warning-500 rounded-full"></div>
                <span className="text-slate-600">
                  <strong>Positioning</strong> shows {
                    (analysis.metrics.non_commercial_net > 0 && analysis.metrics.commercial_net < 0) ? 'classic bullish setup' :
                    (analysis.metrics.non_commercial_net < 0 && analysis.metrics.commercial_net > 0) ? 'classic bearish setup' :
                    'mixed positioning'
                  }
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-success-500 rounded-full"></div>
                <span className="text-slate-600">
                  <strong>Long/Short Ratio:</strong> {analysis.metrics.non_commercial_ratio?.toFixed(2)}
                  ({analysis.metrics.non_commercial_ratio > 1 ? 'Long bias' : 'Short bias'})
                </span>
              </div>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Contrarian Analysis Section */}
      {analysis.analysis.contrarian_analysis && (
        <Card className="shadow-lg border-0">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Target className="w-5 h-5 text-primary-600" />
              <h3 className="text-xl font-semibold text-slate-800">Contrarian COT Analysis</h3>
              <Chip
                size="sm"
                color={analysis.analysis.contrarian_analysis.contrarian_signals > 0 ? 'success' :
                       analysis.analysis.contrarian_analysis.contrarian_signals < 0 ? 'danger' : 'warning'}
                variant="flat"
              >
                {analysis.analysis.contrarian_analysis.contrarian_signals > 0 ? 'Bullish Setup' :
                 analysis.analysis.contrarian_analysis.contrarian_signals < 0 ? 'Bearish Setup' : 'Neutral'}
              </Chip>
            </div>
          </CardHeader>
          <CardBody className="pt-0">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {/* Positioning Extremes */}
              <div className="bg-slate-50 p-4 rounded-lg">
                <h4 className="font-semibold text-slate-700 mb-3 flex items-center gap-2">
                  <Activity className="w-4 h-4" />
                  Positioning Extremes
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Speculative Short:</span>
                    <span className={`font-semibold ${
                      analysis.analysis.positioning_extremes?.speculative_short_pct > 60 ? 'text-danger-600' :
                      analysis.analysis.positioning_extremes?.speculative_short_pct > 55 ? 'text-warning-600' : 'text-slate-600'
                    }`}>
                      {analysis.analysis.positioning_extremes?.speculative_short_pct?.toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Speculative Long:</span>
                    <span className={`font-semibold ${
                      analysis.analysis.positioning_extremes?.speculative_long_pct > 60 ? 'text-success-600' :
                      analysis.analysis.positioning_extremes?.speculative_long_pct > 55 ? 'text-warning-600' : 'text-slate-600'
                    }`}>
                      {analysis.analysis.positioning_extremes?.speculative_long_pct?.toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Extreme Level:</span>
                    <Chip
                      size="sm"
                      color={
                        analysis.analysis.positioning_extremes?.extreme_level === 'HIGH' ? 'danger' :
                        analysis.analysis.positioning_extremes?.extreme_level === 'MODERATE' ? 'warning' : 'default'
                      }
                      variant="flat"
                    >
                      {analysis.analysis.positioning_extremes?.extreme_level}
                    </Chip>
                  </div>
                </div>
              </div>

              {/* Smart Money Signals */}
              <div className="bg-slate-50 p-4 rounded-lg">
                <h4 className="font-semibold text-slate-700 mb-3 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4" />
                  Smart Money Analysis
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Contrarian Signals:</span>
                    <span className={`font-semibold ${
                      analysis.analysis.contrarian_analysis.contrarian_signals > 0 ? 'text-success-600' :
                      analysis.analysis.contrarian_analysis.contrarian_signals < 0 ? 'text-danger-600' : 'text-slate-600'
                    }`}>
                      {analysis.analysis.contrarian_analysis.contrarian_signals}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Smart Money Divergence:</span>
                    <Chip
                      size="sm"
                      color={analysis.analysis.contrarian_analysis.smart_money_divergence ? 'success' : 'default'}
                      variant="flat"
                    >
                      {analysis.analysis.contrarian_analysis.smart_money_divergence ? 'Yes' : 'No'}
                    </Chip>
                  </div>
                  <div className="flex justify-between">
                    <span>Positioning Tension:</span>
                    <Chip
                      size="sm"
                      color={analysis.analysis.contrarian_analysis.positioning_tension ? 'warning' : 'default'}
                      variant="flat"
                    >
                      {analysis.analysis.contrarian_analysis.positioning_tension ? 'Detected' : 'None'}
                    </Chip>
                  </div>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      )}

      {/* Signals Detected */}
      {analysis.analysis.signals && analysis.analysis.signals.length > 0 && (
        <Card className="shadow-lg border-0">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Target className="w-5 h-5 text-primary-600" />
              <h3 className="text-xl font-semibold text-slate-800">Analysis Signals</h3>
              <Chip size="sm" color="primary" variant="flat">
                {analysis.analysis.signals.length}
              </Chip>
            </div>
          </CardHeader>
          <CardBody className="pt-0">
            <div className="space-y-3">
              {analysis.analysis.signals.map((signal, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-lg border-l-4 ${
                    signal.includes('BULLISH') || signal.includes('🔥') || signal.includes('📈')
                      ? 'bg-success-50 border-success-500'
                      : signal.includes('BEARISH') || signal.includes('📉')
                      ? 'bg-danger-50 border-danger-500'
                      : signal.includes('⚠️') || signal.includes('🔥')
                      ? 'bg-warning-50 border-warning-500'
                      : 'bg-primary-50 border-primary-500'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <Chip
                      size="sm"
                      color={getSignalColor(signal)}
                      variant="flat"
                      className="mt-0.5 flex-shrink-0"
                    >
                      {index + 1}
                    </Chip>
                    <p className="text-sm text-slate-700 leading-relaxed">
                      {signal}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Bias Explanation */}
      {analysis.analysis.bias_explanation && (
        <Card className="shadow-xl border-0 bg-white">
          <CardHeader className="pb-4 bg-gradient-to-r from-blue-600 to-indigo-600">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-white/20 rounded-lg">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-white">Why This Bias?</h3>
                <p className="text-blue-100 text-sm mt-1">Understanding the contrarian logic</p>
              </div>
              <div className="ml-auto">
                <Chip size="sm" color="default" variant="flat" className="bg-white/20 text-white border-white/30">
                  Analysis
                </Chip>
              </div>
            </div>
          </CardHeader>
          <CardBody className="pt-0">
            <div className="bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-8 rounded-lg">
              <div
                className="text-slate-800 leading-relaxed"
                style={{
                  fontFamily: "'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif",
                  fontSize: '16px',
                  lineHeight: '1.7',
                  fontWeight: '400'
                }}
              >
                <div className="whitespace-pre-line">
                  {analysis.analysis.bias_explanation}
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      )}

      {/* Catalyst Analysis */}
      {analysis.analysis.catalyst_analysis && analysis.analysis.catalyst_analysis.key_catalysts &&
       analysis.analysis.catalyst_analysis.key_catalysts.length > 0 && (
        <Card className="shadow-xl border-0 bg-white">
          <CardHeader className="pb-4 bg-gradient-to-r from-orange-600 to-red-600">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-white/20 rounded-lg">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-white">Upcoming Catalysts</h3>
                <p className="text-orange-100 text-sm mt-1">Economic events that could impact positioning</p>
              </div>
              <div className="ml-auto">
                <Chip size="sm" color="default" variant="flat" className="bg-white/20 text-white border-white/30">
                  This Week
                </Chip>
              </div>
            </div>
          </CardHeader>
          <CardBody className="pt-0">
            <div className="space-y-6">
              {/* Upcoming Events */}
              <div>
                <h4 className="font-semibold text-slate-700 mb-4 flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  Key Events This Week
                </h4>
                <div className="space-y-3">
                  {analysis.analysis.catalyst_analysis.key_catalysts.slice(0, 5).map((event, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-gradient-to-r from-slate-50 to-gray-50 rounded-lg border border-slate-200">
                      <div className="flex items-center gap-4">
                        <div className="text-center">
                          <div className="text-sm font-semibold text-slate-600">{event.date}</div>
                          <div className="text-xs text-slate-500">{event.time}</div>
                        </div>
                        <div>
                          <div className="font-semibold text-slate-800">{event.event}</div>
                          <div className="text-sm text-slate-600">{event.currency}</div>
                        </div>
                      </div>
                      <Chip
                        size="sm"
                        color={event.impact === 'high' ? 'danger' : event.impact === 'medium' ? 'warning' : 'default'}
                        variant="flat"
                      >
                        {event.impact.toUpperCase()}
                      </Chip>
                    </div>
                  ))}
                </div>
              </div>

              {/* Positioning Impact */}
              {analysis.analysis.catalyst_analysis.positioning_impact && (
                <div>
                  <h4 className="font-semibold text-slate-700 mb-3">Positioning Impact</h4>
                  <div className="bg-gradient-to-r from-yellow-50 to-orange-50 p-4 rounded-lg border border-yellow-200">
                    <div className="whitespace-pre-line text-slate-700 text-sm leading-relaxed">
                      {analysis.analysis.catalyst_analysis.positioning_impact}
                    </div>
                  </div>
                </div>
              )}

              {/* Trading Strategy */}
              {analysis.analysis.catalyst_analysis.trading_strategy && (
                <div>
                  <h4 className="font-semibold text-slate-700 mb-3">Catalyst Trading Strategy</h4>
                  <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-lg border border-green-200">
                    <div className="whitespace-pre-line text-slate-700 text-sm leading-relaxed">
                      {analysis.analysis.catalyst_analysis.trading_strategy}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Trading Implications */}
      <Card className="shadow-lg border-0">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-primary-600" />
            <h3 className="text-xl font-semibold text-slate-800">Trading Implications</h3>
          </div>
        </CardHeader>
        <CardBody className="pt-0">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Strategy Recommendations */}
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-700 mb-3">Strategy Recommendations</h4>
              {analysis.analysis.overall_bias.includes('BULLISH') ? (
                <>
                  <div className="flex items-center gap-3 p-3 bg-success-50 rounded-lg">
                    <TrendingUp className="w-5 h-5 text-success-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Consider LONG USD Index positions</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-success-50 rounded-lg">
                    <Target className="w-5 h-5 text-success-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Look for pullbacks as buying opportunities</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-success-50 rounded-lg">
                    <BarChart3 className="w-5 h-5 text-success-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Monitor for trend continuation patterns</span>
                  </div>
                </>
              ) : analysis.analysis.overall_bias.includes('BEARISH') ? (
                <>
                  <div className="flex items-center gap-3 p-3 bg-danger-50 rounded-lg">
                    <TrendingDown className="w-5 h-5 text-danger-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Consider SHORT USD Index positions</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-danger-50 rounded-lg">
                    <Target className="w-5 h-5 text-danger-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Look for rallies as selling opportunities</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-danger-50 rounded-lg">
                    <BarChart3 className="w-5 h-5 text-danger-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Monitor for breakdown patterns</span>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center gap-3 p-3 bg-warning-50 rounded-lg">
                    <Minus className="w-5 h-5 text-warning-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Neutral positioning recommended</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-warning-50 rounded-lg">
                    <Target className="w-5 h-5 text-warning-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Wait for clearer directional signals</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-warning-50 rounded-lg">
                    <BarChart3 className="w-5 h-5 text-warning-600 flex-shrink-0" />
                    <span className="text-sm text-slate-700">Consider range-bound trading strategies</span>
                  </div>
                </>
              )}
            </div>

            {/* Risk Management */}
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-700 mb-3">Risk Management</h4>

              {analysis.analysis.confidence === 'HIGH' && (
                <div className="flex items-center gap-3 p-3 bg-success-50 rounded-lg">
                  <Target className="w-5 h-5 text-success-600 flex-shrink-0" />
                  <span className="text-sm text-slate-700">HIGH confidence - Signals align strongly</span>
                </div>
              )}

              {analysis.analysis.confidence === 'MEDIUM' && (
                <div className="flex items-center gap-3 p-3 bg-warning-50 rounded-lg">
                  <AlertTriangle className="w-5 h-5 text-warning-600 flex-shrink-0" />
                  <span className="text-sm text-slate-700">MEDIUM confidence - Use moderate position sizes</span>
                </div>
              )}

              {analysis.analysis.confidence === 'LOW' && (
                <div className="flex items-center gap-3 p-3 bg-warning-50 rounded-lg">
                  <AlertTriangle className="w-5 h-5 text-warning-600 flex-shrink-0" />
                  <span className="text-sm text-slate-700">LOW confidence - Use smaller position sizes</span>
                </div>
              )}

              <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                <Activity className="w-5 h-5 text-slate-600 flex-shrink-0" />
                <span className="text-sm text-slate-700">Monitor for changes in positioning</span>
              </div>

              <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                <Calendar className="w-5 h-5 text-slate-600 flex-shrink-0" />
                <span className="text-sm text-slate-700">Review weekly COT updates</span>
              </div>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Disclaimer */}
      <Alert
        color="warning"
        variant="flat"
        startContent={<AlertTriangle size={20} />}
        className="shadow-sm"
      >
        <div className="space-y-2">
          <div className="font-semibold">Important Disclaimer</div>
          <div className="text-sm leading-relaxed">
            This analysis is for educational purposes only and should not be considered as financial advice.
            COT data is historical and doesn't guarantee future price movements. Always conduct your own
            research and consider your risk tolerance before making any trading decisions.
          </div>
        </div>
      </Alert>
    </div>
  );
};

export default AnalysisResults;
