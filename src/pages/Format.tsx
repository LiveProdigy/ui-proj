import { useState } from 'react';
import { Plus, CreditCard as Edit2, Trash2, Mail, MessageSquare, Hash } from 'lucide-react';
import { mockFormats } from '../data/mockData';
import { CommunicationFormat } from '../types';
import FormatWizard from '../components/FormatWizard';

export default function Format() {
  const [formats, setFormats] = useState<CommunicationFormat[]>(mockFormats);
  const [showWizard, setShowWizard] = useState(false);
  const [editingFormat, setEditingFormat] = useState<CommunicationFormat | null>(null);

  const getChannelIcon = (channel: string) => {
    switch (channel) {
      case 'outlook':
        return <Mail className="w-4 h-4" />;
      case 'teams':
        return <MessageSquare className="w-4 h-4" />;
      case 'slack':
        return <Hash className="w-4 h-4" />;
      default:
        return <Mail className="w-4 h-4" />;
    }
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this format?')) {
      setFormats(formats.filter(f => f.id !== id));
    }
  };

  const handleEdit = (format: CommunicationFormat) => {
    setEditingFormat(format);
    setShowWizard(true);
  };

  const handleSaveFormat = (format: CommunicationFormat) => {
    if (editingFormat) {
      setFormats(formats.map(f => f.id === format.id ? format : f));
    } else {
      setFormats([...formats, { ...format, id: Date.now().toString() }]);
    }
    setShowWizard(false);
    setEditingFormat(null);
  };

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Communication Formats</h1>
          <p className="text-gray-600">Define how meeting summaries should be shared</p>
        </div>
        <button
          onClick={() => {
            setEditingFormat(null);
            setShowWizard(true);
          }}
          className="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          <span>Create Format</span>
        </button>
      </div>

      <div className="space-y-4">
        {formats.map((format) => (
          <div
            key={format.id}
            className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-3">
                  <h3 className="text-lg font-semibold text-gray-900">{format.name}</h3>
                  <div className="flex items-center gap-2">
                    {format.channels.map((channel) => (
                      <div
                        key={channel}
                        className="flex items-center gap-1 bg-gray-100 px-2 py-1 rounded-md text-sm text-gray-700"
                      >
                        {getChannelIcon(channel)}
                        <span className="capitalize">{channel}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mb-3">
                  <div className="text-sm text-gray-600 mb-1">Recipients:</div>
                  <div className="flex flex-wrap gap-2">
                    {format.recipients.map((recipient, idx) => (
                      <span
                        key={idx}
                        className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm"
                      >
                        {recipient}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-sm text-gray-600 mb-1">Message Style:</div>
                  <p className="text-gray-700">{format.messageStyle}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 ml-4">
                <button
                  onClick={() => handleEdit(format)}
                  className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <Edit2 className="w-5 h-5" />
                </button>
                <button
                  onClick={() => handleDelete(format.id)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {formats.length === 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
            <div className="text-gray-400 mb-4">
              <FileText className="w-16 h-16 mx-auto" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No formats created yet</h3>
            <p className="text-gray-600 mb-6">Create your first communication format to get started</p>
            <button
              onClick={() => setShowWizard(true)}
              className="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-5 h-5" />
              <span>Create Format</span>
            </button>
          </div>
        )}
      </div>

      {showWizard && (
        <FormatWizard
          format={editingFormat}
          onSave={handleSaveFormat}
          onClose={() => {
            setShowWizard(false);
            setEditingFormat(null);
          }}
        />
      )}
    </div>
  );
}
