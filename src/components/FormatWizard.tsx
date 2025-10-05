import { useState } from 'react';
import { X, Mail, MessageSquare, Hash, ChevronRight, ChevronLeft } from 'lucide-react';
import { CommunicationFormat } from '../types';

interface FormatWizardProps {
  format: CommunicationFormat | null;
  onSave: (format: CommunicationFormat) => void;
  onClose: () => void;
}

export default function FormatWizard({ format, onSave, onClose }: FormatWizardProps) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<Partial<CommunicationFormat>>(
    format || {
      name: '',
      channels: [],
      recipients: [],
      messageStyle: ''
    }
  );

  const availableChannels = [
    { id: 'teams', name: 'Microsoft Teams', icon: MessageSquare, available: true },
    { id: 'outlook', name: 'Outlook Mail', icon: Mail, available: true },
    { id: 'slack', name: 'Slack', icon: Hash, available: true },
    { id: 'discord', name: 'Discord', icon: MessageSquare, available: false },
    { id: 'webhook', name: 'Webhook', icon: Mail, available: false }
  ];

  const sampleRecipients = [
    'john@company.com',
    'sarah@company.com',
    'team@company.com',
    'dev-team',
    'stakeholders'
  ];

  const toggleChannel = (channelId: string) => {
    const channels = formData.channels || [];
    setFormData({
      ...formData,
      channels: channels.includes(channelId)
        ? channels.filter(c => c !== channelId)
        : [...channels, channelId]
    });
  };

  const toggleRecipient = (recipient: string) => {
    const recipients = formData.recipients || [];
    setFormData({
      ...formData,
      recipients: recipients.includes(recipient)
        ? recipients.filter(r => r !== recipient)
        : [...recipients, recipient]
    });
  };

  const handleNext = () => {
    if (step < 3) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleSave = () => {
    if (formData.name && formData.channels && formData.recipients && formData.messageStyle) {
      onSave(formData as CommunicationFormat);
    }
  };

  const canProceed = () => {
    if (step === 1) return (formData.channels?.length || 0) > 0;
    if (step === 2) return (formData.recipients?.length || 0) > 0;
    if (step === 3) return formData.messageStyle && formData.messageStyle.length > 0;
    return false;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {format ? 'Edit Format' : 'Create New Format'}
            </h2>
            <p className="text-sm text-gray-600 mt-1">Step {step} of 3</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {step === 1 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Choose Channels</h3>
              <div className="space-y-3">
                {availableChannels.map((channel) => {
                  const Icon = channel.icon;
                  const isSelected = formData.channels?.includes(channel.id);
                  return (
                    <button
                      key={channel.id}
                      onClick={() => channel.available && toggleChannel(channel.id)}
                      disabled={!channel.available}
                      className={`w-full flex items-center gap-4 p-4 rounded-lg border-2 transition-all ${
                        !channel.available
                          ? 'border-gray-200 bg-gray-50 cursor-not-allowed opacity-50'
                          : isSelected
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className={`p-2 rounded-lg ${isSelected ? 'bg-blue-100' : 'bg-gray-100'}`}>
                        <Icon className={`w-6 h-6 ${isSelected ? 'text-blue-600' : 'text-gray-600'}`} />
                      </div>
                      <div className="flex-1 text-left">
                        <div className="font-medium text-gray-900">{channel.name}</div>
                        {!channel.available && (
                          <div className="text-sm text-gray-500">Coming Soon</div>
                        )}
                      </div>
                      {isSelected && (
                        <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                          <span className="text-white text-sm">✓</span>
                        </div>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {step === 2 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Define Recipients</h3>
              <div className="mb-6">
                <input
                  type="text"
                  placeholder="Enter format name (e.g., Stakeholder Updates)"
                  value={formData.name || ''}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Recipients
                </label>
                <div className="space-y-2">
                  {sampleRecipients.map((recipient) => {
                    const isSelected = formData.recipients?.includes(recipient);
                    return (
                      <label
                        key={recipient}
                        className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:bg-gray-50 cursor-pointer transition-colors"
                      >
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => toggleRecipient(recipient)}
                          className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
                        />
                        <span className="text-gray-900">{recipient}</span>
                      </label>
                    );
                  })}
                </div>
              </div>

              <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                + Add custom recipient
              </button>
            </div>
          )}

          {step === 3 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Define Message Style</h3>
              <p className="text-gray-600 mb-4">
                Describe how you want the AI to generate messages for this format
              </p>
              <textarea
                value={formData.messageStyle || ''}
                onChange={(e) => setFormData({ ...formData, messageStyle: e.target.value })}
                placeholder="Example: Summarize humorously for the client, focusing on key outcomes and next steps. Keep it concise and professional."
                className="w-full h-48 px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <div className="text-sm font-medium text-gray-900 mb-2">Selected Configuration:</div>
                <div className="space-y-2 text-sm text-gray-700">
                  <div>
                    <span className="font-medium">Channels:</span>{' '}
                    {formData.channels?.map(c => c.charAt(0).toUpperCase() + c.slice(1)).join(', ')}
                  </div>
                  <div>
                    <span className="font-medium">Recipients:</span>{' '}
                    {formData.recipients?.length} selected
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
          <button
            onClick={handleBack}
            disabled={step === 1}
            className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
            <span>Back</span>
          </button>

          <div className="flex gap-2">
            {step < 3 ? (
              <button
                onClick={handleNext}
                disabled={!canProceed()}
                className="flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <span>Next</span>
                <ChevronRight className="w-5 h-5" />
              </button>
            ) : (
              <button
                onClick={handleSave}
                disabled={!canProceed()}
                className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Save Format
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
