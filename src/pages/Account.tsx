import { Crown, CreditCard, Calendar, Check } from 'lucide-react';

export default function Account() {
  const features = [
    'Unlimited meeting recordings',
    'AI-powered summaries',
    'Multi-channel distribution',
    'Custom format templates',
    'Priority support',
    'Advanced analytics'
  ];

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Account</h1>
        <p className="text-gray-600">Manage your subscription and billing</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-8 text-white">
            <div className="flex items-center gap-3 mb-4">
              <Crown className="w-8 h-8" />
              <h2 className="text-2xl font-bold">Premium Plan</h2>
            </div>
            <p className="text-blue-100 mb-6">
              You're currently on the Premium plan with full access to all features
            </p>
            <div className="flex items-center gap-6 text-sm">
              <div>
                <div className="text-blue-100 mb-1">Billing Cycle</div>
                <div className="font-semibold">Monthly</div>
              </div>
              <div>
                <div className="text-blue-100 mb-1">Next Billing Date</div>
                <div className="font-semibold">November 5, 2025</div>
              </div>
              <div>
                <div className="text-blue-100 mb-1">Amount</div>
                <div className="font-semibold">$49.99/month</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 flex items-center gap-3">
              <CreditCard className="w-5 h-5 text-gray-600" />
              <h2 className="text-lg font-semibold text-gray-900">Payment Method</h2>
            </div>
            <div className="p-6">
              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-8 bg-gradient-to-br from-gray-700 to-gray-900 rounded flex items-center justify-center text-white text-xs font-bold">
                    VISA
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">Visa ending in 4242</div>
                    <div className="text-sm text-gray-600">Expires 12/2026</div>
                  </div>
                </div>
                <button className="text-blue-600 hover:text-blue-700 font-medium text-sm">
                  Update
                </button>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 flex items-center gap-3">
              <Calendar className="w-5 h-5 text-gray-600" />
              <h2 className="text-lg font-semibold text-gray-900">Billing History</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {[
                { date: 'October 5, 2025', amount: '$49.99', status: 'Paid' },
                { date: 'September 5, 2025', amount: '$49.99', status: 'Paid' },
                { date: 'August 5, 2025', amount: '$49.99', status: 'Paid' }
              ].map((invoice, idx) => (
                <div key={idx} className="px-6 py-4 flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">{invoice.date}</div>
                    <div className="text-sm text-gray-600">{invoice.status}</div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="font-semibold text-gray-900">{invoice.amount}</span>
                    <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                      Download
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Plan Features</h3>
            <ul className="space-y-3">
              {features.map((feature, idx) => (
                <li key={idx} className="flex items-start gap-3">
                  <Check className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{feature}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Usage This Month</h3>
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-600">Meetings Recorded</span>
                  <span className="font-semibold text-gray-900">24</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '48%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-600">Summaries Generated</span>
                  <span className="font-semibold text-gray-900">72</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '72%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-600">Messages Sent</span>
                  <span className="font-semibold text-gray-900">156</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '62%' }}></div>
                </div>
              </div>
            </div>
          </div>

          <button className="w-full bg-gray-100 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-200 transition-colors">
            Manage Subscription
          </button>
        </div>
      </div>
    </div>
  );
}
