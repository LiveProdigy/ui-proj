import { useState } from 'react';
import { X, ChevronRight, ChevronLeft, Plus, Trash2 } from 'lucide-react';
import { CommunicationFormat } from '../types';
import teamsIcon from '../assets/microsoft-teams-svgrepo-com.svg';
import outlookIcon from '../assets/ms-outlook-svgrepo-com.svg';
import gmailIcon from '../assets/gmail-svgrepo-com.svg';
import slackIcon from '../assets/slack-svgrepo-com.svg';

interface FormatWizardProps {
  format: CommunicationFormat | null;
  onSave: (format: CommunicationFormat) => void;
  onClose: () => void;
}

export default function FormatWizard({ format, onSave, onClose }: FormatWizardProps) {
  const [step, setStep] = useState(1);
  const [selectedChannel, setSelectedChannel] = useState<string>('');
  const [recipientGroups, setRecipientGroups] = useState<Array<{ recipients: string[]; description: string; tags: string }>>([{ recipients: [], description: '', tags: '' }]);
  const [channelStyles, setChannelStyles] = useState<Record<string, string>>({});
  const [formData, setFormData] = useState<Partial<CommunicationFormat>>(
    format || {
      name: '',
      channels: [],
      recipients: [],
      messageStyle: ''
    }
  );

  const availableChannels = [
    { id: 'teams', name: 'Microsoft Teams', icon: teamsIcon },
    { id: 'outlook', name: 'Outlook Mail', icon: outlookIcon },
    { id: 'gmail', name: 'Gmail', icon: gmailIcon },
    { id: 'slack', name: 'Slack', icon: slackIcon }
  ];

  const sampleRecipients = [
    'john@company.com',
    'sarah@company.com',
    'team@company.com',
    'dev-team',
    'stakeholders',
    'clients@company.com'
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
    if (formData.name && formData.channels && formData.recipients) {
      onSave({ ...formData, messageStyle: JSON.stringify(channelStyles) } as CommunicationFormat);
    }
  };

  const addRecipientGroup = () => {
    setRecipientGroups([...recipientGroups, { recipients: [], description: '', tags: '' }]);
  };

  const removeRecipientGroup = (index: number) => {
    setRecipientGroups(recipientGroups.filter((_, i) => i !== index));
  };

  const updateRecipientGroup = (index: number, field: string, value: any) => {
    const updated = [...recipientGroups];
    updated[index] = { ...updated[index], [field]: value };
    setRecipientGroups(updated);
  };

  const canProceed = () => {
    if (step === 1) return (formData.channels?.length || 0) > 0;
    if (step === 2) return formData.name && recipientGroups.some(g => g.recipients.length > 0);
    if (step === 3) return formData.channels?.every(ch => channelStyles[ch]?.length > 0);
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
                  const isSelected = formData.channels?.includes(channel.id);
                  return (
                    <button
                      key={channel.id}
                      onClick={() => toggleChannel(channel.id)}
                      className={`w-full flex items-center gap-4 p-4 rounded-lg border-2 transition-all ${
                        isSelected
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <img src={channel.icon} alt={channel.name} className="w-8 h-8" />
                      <div className="flex-1 text-left">
                        <div className="font-medium text-gray-900">{channel.name}</div>
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

              <div className="flex gap-2 mb-4 border-b border-gray-200">
                {formData.channels?.map((ch) => {
                  const channel = availableChannels.find(c => c.id === ch);
                  return (
                    <button
                      key={ch}
                      onClick={() => setSelectedChannel(ch)}
                      className={`flex items-center gap-2 px-4 py-2 border-b-2 transition-colors ${
                        selectedChannel === ch
                          ? 'border-blue-600 text-blue-600'
                          : 'border-transparent text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      <img src={channel?.icon} alt={ch} className="w-4 h-4" />
                      <span className="capitalize font-medium">{ch}</span>
                    </button>
                  );
                })}
              </div>

              {selectedChannel && (
                <div className="space-y-4">
                  {recipientGroups.map((group, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-medium text-gray-900">Recipient Group {idx + 1}</h4>
                        {recipientGroups.length > 1 && (
                          <button
                            onClick={() => removeRecipientGroup(idx)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>

                      <div className="space-y-3">
                        <div>
                          <label className="block text-xs font-medium text-gray-700 mb-1">
                            Recipients
                          </label>
                          <div className="space-y-1">
                            {sampleRecipients.map((recipient) => {
                              const isSelected = group.recipients.includes(recipient);
                              return (
                                <label
                                  key={recipient}
                                  className="flex items-center gap-2 text-sm cursor-pointer"
                                >
                                  <input
                                    type="checkbox"
                                    checked={isSelected}
                                    onChange={(e) => {
                                      const newRecipients = e.target.checked
                                        ? [...group.recipients, recipient]
                                        : group.recipients.filter(r => r !== recipient);
                                      updateRecipientGroup(idx, 'recipients', newRecipients);
                                      const allRecipients = recipientGroups.flatMap(g => g.recipients);
                                      setFormData({ ...formData, recipients: [...new Set([...allRecipients, ...newRecipients])] });
                                    }}
                                    className="w-4 h-4 text-blue-600 rounded"
                                  />
                                  <span className="text-gray-900">{recipient}</span>
                                </label>
                              );
                            })}
                          </div>
                        </div>

                        <div>
                          <label className="block text-xs font-medium text-gray-700 mb-1">
                            Description
                          </label>
                          <input
                            type="text"
                            value={group.description}
                            onChange={(e) => updateRecipientGroup(idx, 'description', e.target.value)}
                            placeholder="Brief description"
                            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                        </div>

                        <div>
                          <label className="block text-xs font-medium text-gray-700 mb-1">
                            Tags (optional)
                          </label>
                          <input
                            type="text"
                            value={group.tags}
                            onChange={(e) => updateRecipientGroup(idx, 'tags', e.target.value)}
                            placeholder="e.g., urgent, weekly"
                            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                      </div>
                    </div>
                  ))}

                  <button
                    onClick={addRecipientGroup}
                    className="flex items-center gap-2 text-sm text-blue-600 hover:text-blue-700 font-medium"
                  >
                    <Plus className="w-4 h-4" />
                    Add another recipient group
                  </button>
                </div>
              )}

              {!selectedChannel && formData.channels?.length === 0 && (
                <p className="text-sm text-gray-500 text-center py-8">Please select a channel above</p>
              )}
            </div>
          )}

          {step === 3 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Define Message Style</h3>

              <div className="flex gap-2 mb-4 border-b border-gray-200">
                {formData.channels?.map((ch) => {
                  const channel = availableChannels.find(c => c.id === ch);
                  return (
                    <button
                      key={ch}
                      onClick={() => setSelectedChannel(ch)}
                      className={`flex items-center gap-2 px-4 py-2 border-b-2 transition-colors ${
                        selectedChannel === ch
                          ? 'border-blue-600 text-blue-600'
                          : 'border-transparent text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      <img src={channel?.icon} alt={ch} className="w-4 h-4" />
                      <span className="capitalize font-medium">{ch}</span>
                    </button>
                  );
                })}
              </div>

              {selectedChannel && (
                <div>
                  <p className="text-sm text-gray-600 mb-3">
                    Define the message style for <span className="font-semibold capitalize">{selectedChannel}</span>
                  </p>
                  <textarea
                    value={channelStyles[selectedChannel] || ''}
                    onChange={(e) => setChannelStyles({ ...channelStyles, [selectedChannel]: e.target.value })}
                    placeholder="Example: Summarize professionally for the client, focusing on key outcomes and next steps. Keep it concise."
                    className="w-full h-40 px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  />
                </div>
              )}

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <div className="text-sm font-medium text-gray-900 mb-2">Configuration Summary:</div>
                <div className="space-y-2 text-sm text-gray-700">
                  <div>
                    <span className="font-medium">Format Name:</span> {formData.name}
                  </div>
                  <div>
                    <span className="font-medium">Channels:</span>{' '}
                    {formData.channels?.map(c => c.charAt(0).toUpperCase() + c.slice(1)).join(', ')}
                  </div>
                  <div>
                    <span className="font-medium">Styles Defined:</span>{' '}
                    {Object.keys(channelStyles).length} of {formData.channels?.length}
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
