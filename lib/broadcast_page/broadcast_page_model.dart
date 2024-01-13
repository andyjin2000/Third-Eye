import '/backend/backend.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'broadcast_page_widget.dart' show BroadcastPageWidget;
import 'package:flutter/material.dart';

class BroadcastPageModel extends FlutterFlowModel<BroadcastPageWidget> {
  ///  State fields for stateful widgets in this page.

  final unfocusNode = FocusNode();
  // Stores action output result for [Backend Call - Create Document] action in MuxBroadcast widget.
  StreamsRecord? muxStreamOutput;
  // State field(s) for TextField widget.
  FocusNode? textFieldFocusNode;
  TextEditingController? textController;
  String? Function(BuildContext, String?)? textControllerValidator;
  // Stores action output result for [Backend Call - Create Document] action in Button widget.
  StreamsRecord? broadcastInstruction;

  /// Initialization and disposal methods.

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    unfocusNode.dispose();
    textFieldFocusNode?.dispose();
    textController?.dispose();
  }

  /// Action blocks are added here.

  /// Additional helper methods are added here.
}
