import React from 'react';
import { Card, CardHeader, CardBody } from '@nextui-org/react';
import { Activity } from 'lucide-react';

const Header = () => {
  return (
    <Card className="shadow-lg border-0">
      <CardHeader className="pb-4">
        <div className="flex flex-col items-center text-center w-full">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-primary-100 rounded-full">
              <Activity className="w-8 h-8 text-primary-600" />
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-slate-800">
              Multi-Asset COT Analyzer
            </h1>
          </div>
          <p className="text-slate-600 text-lg max-w-3xl leading-relaxed">
            Analyze CFTC Commitments of Traders data for multiple assets including USD Index,
            commodities, currencies, and indices to identify directional bias and trading opportunities
            based on institutional positioning.
          </p>
        </div>
      </CardHeader>
    </Card>
  );
};

export default Header;
