
import React, { useState } from 'react';
import { SafeAreaView, View, Text, Button, TextInput, Alert } from 'react-native';
import axios from 'axios';

const API = process.env.EXPO_PUBLIC_API || 'http://localhost:8000';

export default function App() {
  const [email, setEmail] = useState('user@example.com');
  const [userId, setUserId] = useState<number | null>(null);
  const [consent, setConsent] = useState(false);

  async function register() {
    const resp = await axios.post(`${API}/users`, { email });
    setUserId(resp.data.id);
    Alert.alert('Registered', `User ID: ${resp.data.id}`);
  }

  async function giveConsent() {
    if (!userId) return;
    await axios.post(`${API}/consent/${userId}`, { analytics: true, marketing: true });
    setConsent(true);
    Alert.alert('Consent', 'Analytics + marketing consent granted.');
  }

  async function sendEvent(type: string, properties: object = {}) {
    if (!userId) {
      Alert.alert('Error', 'Register first.');
      return;
    }
    try {
      await axios.post(`${API}/events`, { user_id: userId, type, properties });
      Alert.alert('Event', `Sent: ${type}`);
    } catch (e: any) {
      Alert.alert('Event Error', e?.response?.data?.detail || 'Unknown error');
    }
  }

  return (
    <SafeAreaView style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: '600' }}>Pulse — Demo MVP</Text>
      <View style={{ height: 12 }} />
      <Text>Email</Text>
      <TextInput
        value={email}
        onChangeText={setEmail}
        style={{ borderWidth: 1, borderRadius: 8, padding: 8 }}
        autoCapitalize="none"
      />
      <View style={{ height: 8 }} />
      <Button title="Register" onPress={register} />
      <View style={{ height: 8 }} />
      <Button title="Grant Consent" onPress={giveConsent} />
      <View style={{ height: 16 }} />
      <Button title="Event: app_open" onPress={() => sendEvent('app_open')} />
      <View style={{ height: 8 }} />
      <Button title="Event: sponsor_cta_click" onPress={() => sendEvent('sponsor_cta_click', { sponsor: 'BrandX' })} />
      <View style={{ height: 8 }} />
      <Button title="Event: purchase" onPress={() => sendEvent('purchase', { item: 'Pulse+ Upgrade', price: 4.99 })} />
      <View style={{ height: 24 }} />
      <Text style={{ color: 'gray' }}>Consent: {consent ? 'granted' : 'not granted'}</Text>
    </SafeAreaView>
  );
}
