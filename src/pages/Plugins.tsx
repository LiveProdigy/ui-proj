import { useState } from 'react';
import { Plus, CreditCard as Edit2, Trash2, Power } from 'lucide-react';
import { mockPlugins } from '../data/mockData';
import { Plugin } from '../types';
import PluginConfigModal from '../components/PluginConfigModal';
import teamsIcon from '../assets/microsoft-teams-svgrepo-com.svg';
import outlookIcon from '../assets/ms-outlook-svgrepo-com.svg';
import gmailIcon from '../assets/gmail-svgrepo-com.svg';
import slackIcon from '../assets/slack-svgrepo-com.svg';

export default function Plugins() {
  const [plugins, setPlugins] = useState<Plugin[]>(mockPlugins);
  const [showConfigModal, setShowConfigModal] = useState(false);

  const getPluginIcon = (type: string) => {
    switch (type) {
      case 'teams':
        return teamsIcon;
      case 'outlook':
        return outlookIcon;
      case 'slack':
        return slackIcon;
      case 'gmail':
        return gmailIcon;
      default:
        return gmailIcon;
    }
  };

  const getPluginCount = (type: string) => {
    return plugins.filter(p => p.type === type).length;
  };

  const formatLastSynced = (date: string) => {
    const now = new Date();
    const syncDate = new Date(date);
    const diffMs = now.getTime() - syncDate.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);

    if (diffMins < 60) return `${diffMins} mins ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    return syncDate.toLocaleDateString();
  };

  const togglePlugin = (id: string) => {
    setPlugins(plugins.map(p =>
      p.id === id ? { ...p, isActive: !p.isActive } : p
    ));
  };

  const deletePlugin = (id: string) => {
    if (confirm('Are you sure you want to remove this plugin?')) {
      setPlugins(plugins.filter(p => p.id !== id));
    }
  };

  const pluginTypes = [
    { type: 'teams', name: 'Microsoft Teams', icon: teamsIcon },
    { type: 'outlook', name: 'Outlook', icon: outlookIcon },
    { type: 'slack', name: 'Slack', icon: slackIcon },
    { type: 'gmail', name: 'Gmail', icon: gmailIcon }
  ];

  const handleSavePlugin = (config: { type: string; name: string; schema: string }) => {
    const newPlugin: Plugin = {
      id: Date.now().toString(),
      type: config.type as any,
      profileName: config.name,
      schema: config.schema,
      isActive: true,
      lastSynced: new Date().toISOString()
    };
    setPlugins([...plugins, newPlugin]);
    setShowConfigModal(false);
  };

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Plugins</h1>
          <p className="text-gray-600">Manage your integrations and connections</p>
        </div>
        <button
          onClick={() => setShowConfigModal(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          <span>Add Plugin</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {pluginTypes.map((plugin) => (
          <div
            key={plugin.type}
            className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex flex-col items-center text-center">
              <img src={plugin.icon} alt={plugin.name} className="w-12 h-12 mb-3" />
              <h3 className="font-semibold text-gray-900 mb-1">{plugin.name}</h3>
              <p className="text-sm text-gray-600">
                {getPluginCount(plugin.type)} profile{getPluginCount(plugin.type) !== 1 ? 's' : ''}
              </p>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Connected Profiles</h2>
        </div>

        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Plugin</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Profile Name</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Schema</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Status</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Last Synced</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {plugins.map((plugin) => (
              <tr key={plugin.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <img src={getPluginIcon(plugin.type)} alt={plugin.type} className="w-6 h-6" />
                    <span className="font-medium text-gray-900 capitalize">{plugin.type}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="text-gray-900">{plugin.profileName}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full capitalize">
                    {plugin.schema || 'N/A'}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <div
                      className={`w-2 h-2 rounded-full ${
                        plugin.isActive ? 'bg-green-500' : 'bg-gray-300'
                      }`}
                    ></div>
                    <span className={plugin.isActive ? 'text-green-600' : 'text-gray-500'}>
                      {plugin.isActive ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="text-gray-600">{formatLastSynced(plugin.lastSynced)}</span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => togglePlugin(plugin.id)}
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                      title={plugin.isActive ? 'Disable' : 'Enable'}
                    >
                      <Power className="w-5 h-5" />
                    </button>
                    <button className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                      <Edit2 className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => deletePlugin(plugin.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showConfigModal && (
        <PluginConfigModal
          onClose={() => setShowConfigModal(false)}
          onSave={handleSavePlugin}
        />
      )}
    </div>
  );
}
