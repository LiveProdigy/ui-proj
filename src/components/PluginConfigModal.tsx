import { useState } from 'react';
import { X } from 'lucide-react';
import teamsIcon from '../assets/microsoft-teams-svgrepo-com.svg';
import outlookIcon from '../assets/ms-outlook-svgrepo-com.svg';
import gmailIcon from '../assets/gmail-svgrepo-com.svg';
import slackIcon from '../assets/slack-svgrepo-com.svg';

interface PluginConfigModalProps {
  onClose: () => void;
  onSave: (config: { type: string; name: string; schema: string }) => void;
}

export default function PluginConfigModal({ onClose, onSave }: PluginConfigModalProps) {
  const [step, setStep] = useState<'select' | 'configure'>('select');
  const [selectedType, setSelectedType] = useState<string>('');
  const [name, setName] = useState('');
  const [schema, setSchema] = useState('professional');
  const [isLoading, setIsLoading] = useState(false);

  const pluginTypes = [
    { type: 'teams', name: 'Microsoft Teams', icon: teamsIcon },
    { type: 'outlook', name: 'Outlook', icon: outlookIcon },
    { type: 'gmail', name: 'Gmail', icon: gmailIcon },
    { type: 'slack', name: 'Slack', icon: slackIcon }
  ];

  const handleSelectPlugin = (type: string) => {
    setSelectedType(type);
    setStep('configure');
  };

  const handleSave = () => {
    setIsLoading(true);
    setTimeout(() => {
      onSave({ type: selectedType, name, schema });
      setIsLoading(false);
      onClose();
    }, 1500);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl w-full max-w-md">
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">
            {step === 'select' ? 'Select Plugin' : 'Configure Connection'}
          </h2>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6">
          {step === 'select' && (
            <div className="space-y-3">
              {pluginTypes.map((plugin) => (
                <button
                  key={plugin.type}
                  onClick={() => handleSelectPlugin(plugin.type)}
                  className="w-full flex items-center gap-4 p-4 rounded-lg border-2 border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all"
                >
                  <img src={plugin.icon} alt={plugin.name} className="w-8 h-8" />
                  <span className="font-medium text-gray-900">{plugin.name}</span>
                </button>
              ))}
            </div>
          )}

          {step === 'configure' && (
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                <img
                  src={pluginTypes.find(p => p.type === selectedType)?.icon}
                  alt={selectedType}
                  className="w-8 h-8"
                />
                <span className="font-semibold text-gray-900">
                  {pluginTypes.find(p => p.type === selectedType)?.name}
                </span>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Connection Name
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g., Work Account"
                  className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Schema (Optional)
                </label>
                <select
                  value={schema}
                  onChange={(e) => setSchema(e.target.value)}
                  className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="professional">Professional</option>
                  <option value="personal">Personal</option>
                  <option value="company">Company</option>
                </select>
              </div>

              <button
                onClick={handleSave}
                disabled={!name || isLoading}
                className="w-full bg-blue-600 text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {isLoading ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Connecting...</span>
                  </div>
                ) : (
                  'Connect'
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
