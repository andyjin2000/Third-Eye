import 'dart:async';

import 'package:collection/collection.dart';

import '/backend/schema/util/firestore_util.dart';
import '/backend/schema/util/schema_util.dart';

import 'index.dart';

class StreamsRecord extends FirestoreRecord {
  StreamsRecord._(
    super.reference,
    super.data,
  ) {
    _initializeFields();
  }

  // "is_live" field.
  bool? _isLive;
  bool get isLive => _isLive ?? false;
  bool hasIsLive() => _isLive != null;

  // "playback_name" field.
  String? _playbackName;
  String get playbackName => _playbackName ?? '';
  bool hasPlaybackName() => _playbackName != null;

  // "playback_url" field.
  String? _playbackUrl;
  String get playbackUrl => _playbackUrl ?? '';
  bool hasPlaybackUrl() => _playbackUrl != null;

  // "timestamp" field.
  DateTime? _timestamp;
  DateTime? get timestamp => _timestamp;
  bool hasTimestamp() => _timestamp != null;

  // "uid" field.
  String? _uid;
  String get uid => _uid ?? '';
  bool hasUid() => _uid != null;

  // "instruction" field.
  String? _instruction;
  String get instruction => _instruction ?? '';
  bool hasInstruction() => _instruction != null;

  void _initializeFields() {
    _isLive = snapshotData['is_live'] as bool?;
    _playbackName = snapshotData['playback_name'] as String?;
    _playbackUrl = snapshotData['playback_url'] as String?;
    _timestamp = snapshotData['timestamp'] as DateTime?;
    _uid = snapshotData['uid'] as String?;
    _instruction = snapshotData['instruction'] as String?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('streams');

  static Stream<StreamsRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => StreamsRecord.fromSnapshot(s));

  static Future<StreamsRecord> getDocumentOnce(DocumentReference ref) =>
      ref.get().then((s) => StreamsRecord.fromSnapshot(s));

  static StreamsRecord fromSnapshot(DocumentSnapshot snapshot) =>
      StreamsRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static StreamsRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      StreamsRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'StreamsRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is StreamsRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createStreamsRecordData({
  bool? isLive,
  String? playbackName,
  String? playbackUrl,
  DateTime? timestamp,
  String? uid,
  String? instruction,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'is_live': isLive,
      'playback_name': playbackName,
      'playback_url': playbackUrl,
      'timestamp': timestamp,
      'uid': uid,
      'instruction': instruction,
    }.withoutNulls,
  );

  return firestoreData;
}

class StreamsRecordDocumentEquality implements Equality<StreamsRecord> {
  const StreamsRecordDocumentEquality();

  @override
  bool equals(StreamsRecord? e1, StreamsRecord? e2) {
    return e1?.isLive == e2?.isLive &&
        e1?.playbackName == e2?.playbackName &&
        e1?.playbackUrl == e2?.playbackUrl &&
        e1?.timestamp == e2?.timestamp &&
        e1?.uid == e2?.uid &&
        e1?.instruction == e2?.instruction;
  }

  @override
  int hash(StreamsRecord? e) => const ListEquality().hash([
        e?.isLive,
        e?.playbackName,
        e?.playbackUrl,
        e?.timestamp,
        e?.uid,
        e?.instruction
      ]);

  @override
  bool isValidKey(Object? o) => o is StreamsRecord;
}
